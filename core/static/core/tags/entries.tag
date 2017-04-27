<entries>
    <p class="mb-4 clearfix">
        <button class="btn btn-primary btn-sm mr-2" onclick={ timer }>
            { timerState } Timer
            <i class="fa fa-clock-o ml-2" aria-hidden="true"></i>
            <span class="timer text-bold">{ hours }h { minutes }m { seconds }s</span>
        </button>

        <pager update="{ getEntries }"/>
    </p>


    <form onsubmit={ submitEntry }>
        <div class="row bg-primary form-row mb-2">
            <div class="col-sm-3">
                <select class="custom-select bg-primary" ref="project">
                    <option each={ projects } value={ url }>{ name } ({ client_details.name })</option>
                </select>
            </div>
            <div class="col-sm-4">
                <input type="text" class="form-control form-control-lg bg-primary" ref="note" placeholder="Note">
            </div>
            <div class="col-sm-2">
                <input type="text" class="form-control form-control-lg bg-primary" ref="duration" placeholder="0:00" value="{ timerDuration }">
            </div>
            <div class="col-sm-3">
                <button type="submit" class="btn btn-primary btn-lg">
                    <i class="fa fa-plus" aria-hidden="true"></i> Add
                </button>
            </div>
        </div>
    </form>

    <div class="row bg-inverse py-2 mb-2 text-white">
        <div class="col-sm-2">
            <strong>Date</strong>
        </div>
        <div class="col-sm-2">
            <strong>User</strong>
        </div>
        <div class="col-sm-3">
            <strong>Project</strong>
        </div>
        <div class="col-sm-3">
            <strong>Note</strong>
        </div>
        <div class="col-sm-2">
            <strong>Duration</strong>
        </div>
    </div>
    <div class="row bg-faded py-2 mb-2" each={ entries }>
        <div class="col-sm-2">
            { date }
        </div>
        <div class="col-sm-2">
            { user_details.username }
        </div>
        <div class="col-sm-3">
            { project_details.name }
        </div>
        <div class="col-sm-3">
            { note }
        </div>
        <div class="col-sm-2">
            { duration }
        </div>
    </div>
    <div class="row bg-success text-white py-2">
        <div class="offset-sm-8 col-sm-2 text-right">
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
                seconds: ++self.seconds
            });
        }


        timer(e) {
            if (self.timerState === 'Start') {
                self.timerState = 'Stop';
                interval = setInterval(self.tick, 1000);
            } else {
                self.timerState = 'Start';
                clearInterval(interval);
                self.timerDuration = pad(self.hours) + ':' + pad(self.minutes) + ':' + pad(self.seconds);
                self.hours = 0;
                self.minutes = 0;
                self.seconds = 0;
            }
        }


        getEntries(url) {
            url = (typeof url !== 'undefined') ? url : entriesApiUrl;

            let entries = quickFetch(url);
            let users = quickFetch(usersApiUrl);
            let projects = quickFetch(projectsApiUrl);

            Promise.all([entries, users, projects]).then(function(e) {
                self.update({
                    entries: e[0].results,
                    users: promote(userId, e[1].results),
                    projects: e[2].results,
                    totalTime: getTotalTime(e[0].results),
                    next: e[0].next,
                    previous: e[0].previous
                });

                $('.loading, .entries-table').toggleClass('d-none');
                $('.date-input').pickadate({
                    format: 'yyyy-mm-dd',
                    onStart: function() {
                        this.set('select', new Date());
                    }
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
                self.update();
            });
        }


        self.getEntries();
    </script>
</entries>
