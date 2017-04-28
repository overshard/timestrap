<entries>
    <p class="mb-4 clearfix row-fix">
        <pager update="{ getEntries }"/>
    </p>


    <form onsubmit={ submitEntry }>
        <div class="row form-row mb-5 shadow-muted">
            <div class="col-sm-3">
                <select class="custom-select" ref="project">
                    <option value='' class="text-muted">Project</option>
                    <option each={ projects } value={ url }>{ name }</option>
                </select>
            </div>
            <div class="col-sm-5">
                <input type="text" class="form-control form-control-lg" ref="note" placeholder="Note">
            </div>
            <div class="col-sm-2">
                <input type="text" class="form-control form-control-lg" onkeyup={ timer } ref="duration" placeholder="0:00" value="{ timerDuration }">
            </div>
            <div class="col-sm-2">
                <button type="submit" class="btn btn-success btn-lg" onclick={ timer }>{ timerState }</button>
            </div>
        </div>
    </form>

    <div class="mb-5" each={ dates }>
        <h5 class="text-muted">{ mainDate }</h5>
        <div class="entries-rows shadow-muted row-fix">
            <div class="row py-2" each={ entries } if={ mainDate === date }>
                <div class="col-sm-3">
                    <div class="text-muted small">
                        { project_details.client_details.name }
                    </div>
                    { project_details.name }
                </div>
                <div class="col-sm-5 d-flex align-self-end">
                    { note }
                </div>
                <div class="col-sm-2 d-flex align-self-end">
                    { duration }
                </div>
                <div class="col-sm-2 d-flex align-self-center justify-content-end">
                    <button class="btn btn-secondary dropdown-toggle" type="button" id="entry-edit-menu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
                    </button>
                    <div class="dropdown-menu" aria-labelledby="entry-edit-menu">
                        <a class="dropdown-item" href="#">Restart</a>
                        <a class="dropdown-item" href="#">Edit</a>
                        <a class="dropdown-item" href="#">Delete</a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row bg-success text-white py-2 my-5">
        <div class="offset-sm-6 col-sm-2 text-right">
            <strong>Total</strong>
        </div>
        <div class="col-sm-2">
            <strong>{ totalTime }</strong>
        </div>
    </div>

    <script>
        var self = this;
        var interval;
        self.timerState = 'Start';
        self.hours = 0;
        self.minutes = 0;
        self.seconds = 0;



        // TODO: There has to be a better way
        tick() {
            if (self.seconds === 60) {
                ++self.minutes;
                self.seconds = -1;
            }
            if (self.minutes === 60) {
                ++self.hours;
                self.minutes = 0;
            }
            self.update({
                hours: self.hours,
                minutes: self.minutes,
                seconds: ++self.seconds,
                timerDuration: pad(self.hours) + ':' + pad(self.minutes) + ':' + pad(self.seconds)
            });
        }


        timer(e) {
            let duration = self.refs.duration.value;
            // TODO: Cleanup
            if (duration && self.timerState !== 'Stop') {
                self.timerState == 'Start';
            } else {
                if (self.timerState === 'Start') {
                    self.timerState = 'Stop';
                    interval = setInterval(self.tick, 1000);
                    e.preventDefault();
                } else {
                    self.timerState = 'Add';
                    clearInterval(interval);
                    self.timerDuration = pad(self.hours) + ':' + pad(self.minutes);
                    self.hours = 0;
                    self.minutes = 0;
                    self.seconds = 0;
                    e.preventDefault();
                }
            }
        }


        getEntries(url) {
            url = (typeof url !== 'undefined') ? url : entriesApiUrl;

            let entries = quickFetch(url);
            let users = quickFetch(usersApiUrl);
            let projects = quickFetch(projectsApiUrl);

            Promise.all([entries, users, projects]).then(function(e) {
                let dates = [];
                $.each(e[0].results, function(i, el) {
                    if ($.inArray(el.date, dates) === -1) {
                        dates.push(el.date);
                    }
                });
                // Doing this in another loop and not the previous because
                // inArray doesn't seem to match objects very well here.
                let dateObjects = [];
                $.each(dates, function(i, el) {
                    dateObjects.push({mainDate: el});
                });

                self.update({
                    dates: dateObjects,
                    entries: e[0].results,
                    users: promote(userId, e[1].results),
                    projects: e[2].results,
                    totalTime: getTotalTime(e[0].results),
                    next: e[0].next,
                    previous: e[0].previous
                });
            });
        }


        submitEntry(e) {
            e.preventDefault();
            let csrfToken = Cookies.get('csrftoken');
            let body = {
                user: usersApiUrl + userId + '/',
                duration: self.refs.duration.value,
                note: self.refs.note.value,
                project: self.refs.project.value
            }
            quickFetch(entriesApiUrl, 'post', body).then(function(data) {
                self.refs.duration.value = '';
                self.refs.note.value = '';
                self.entries.unshift(data);
                self.timerState = 'Start';
                self.update();
            });
        }


        self.getEntries();
    </script>
</entries>
