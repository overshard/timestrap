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
        <table class="entries-table table table-striped table-sm w-100 d-none">
            <thead class="thead-inverse">
                <tr>
                    <th>Date</th>
                    <th>User</th>
                    <th>Duration</th>
                    <th>Note</th>
                    <th>Project</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr class="table-info">
                    <td>
                        <input type="text" class="date-input form-control form-control-sm" ref="date" placeholder="Date">
                    </td>
                    <td>
						<select class="user-select" ref="user">
							<option each={ users } value={ url }>{ username }</option>
						</select>
                    </td>
                    <td>
                        <input type="text" class="form-control form-control-sm" ref="duration" placeholder="Duration" value="{ timerDuration }">
                    </td>
                    <td>
                        <input type="text" class="form-control form-control-sm" ref="note" placeholder="Note">
                    </td>
                    <td>
						<select class="project-select" ref="project">
                            <option each={ projects } value={ url }>{ name } ({ client_details.name })</option>
						</select>
                    </td>
                    <td class="text-right">
                        <button type="submit" class="btn btn-primary btn-sm">Add</button>
                    </td>
                </tr>
                <tr each={ entries }>
                    <td>{ date }</td>
                    <td>{ user_details.username }</td>
                    <td>{ duration }</td>
                    <td>{ note }</td>
                    <td>{ project_details.name }</td>
                    <td class="text-right"></td>
                </tr>
                <tr class="table-active">
                    <td></td>
                    <td><strong>Total</strong></td>
                    <td><strong>{ totalTime }</strong></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
            </tbody>
        </table>
    </form>

    <p class="loading text-center my-5">
        <i class="fa fa-spinner" aria-hidden="true"></i>
    </p>

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

            $('.loading, .entries-table').toggleClass('d-none');

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
				$('.user-select').chosen({width: '100%'});
				$('.project-select').chosen({width: '100%'});
            });
        }


        submitEntry(e) {
            e.preventDefault();
            let csrfToken = Cookies.get('csrftoken');
            let body = {
                date: self.refs.date.value,
                user: self.refs.user.value,
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
