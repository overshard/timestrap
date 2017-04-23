<entries>
    <p class="mb-4 clearfix">
        <button class="btn btn-primary btn-sm pull-right"
            data-url="{ next }"
            if={ next }
            onclick={ entriesPage }>
            Next <i class="fa fa-arrow-right" aria-hidden="true"></i>
        </button>

        <button class="btn btn-primary btn-sm pull-right mr-1"
            data-url="{ previous }"
            if={ previous }
            onclick={ entriesPage }>
            <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous
        </button>

        <a class="btn btn-primary btn-sm pull-right mr-1" href='/entries/csv/'>
            CSV Export
        </a>

        <button class="btn btn-primary btn-sm mr-2" onclick={ timer }>
            { timerState } Timer
            <i class="fa fa-clock-o ml-2" aria-hidden="true"></i>
            <span class="timer text-bold">{ hours }h { minutes }m { seconds }s</span>
        </button>
    </p>

    <form onsubmit={ submitEntry }>
        <table class="entries-table table table-striped table-sm w-100 d-none">
            <thead class="thead-inverse">
                <tr>
                    <th>Date</th>
                    <th>User</th>
                    <th>Duration</th>
                    <th>Note</th>
                    <th>Task</th>
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
						<select class="task-select" ref="task">
							<option each={ tasks } value={ url }>{ name }</option>
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
                    <td>{ task_details.name }</td>
                    <td class="text-right"><a class="btn btn-primary btn-sm" onclick={ deleteEntry } data-url={ url }><i class="fa fa-trash" aria-hidden="true"></i></a></td>
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
        var tag = this;
        var loading;
        var entriesTable;
        var interval;
        tag.timerState = 'Start';
        tag.hours = 0;
        tag.minutes = 0;
        tag.seconds = 0;
        tag.timerDuration = '00:00:00';

        getTimeInSeconds(time) {
            let timeInSeconds = 0;
            time = time.split(':');
            timeInSeconds += parseInt(time[0])*3600;
            timeInSeconds += parseInt(time[1])*60;
            timeInSeconds += parseInt(time[2]);
            return timeInSeconds;
        }

        pad(num) {
            num = num.toString();
            if (num.length === 1) {
                num = '0' + num;
            }
            return num
        }

        tick() {
            if (tag.seconds === 60) {
                ++tag.minutes;
                tag.seconds = -1;
            }
            if (tag.minutes === 60) {
                ++tag.hours;
                tag.minutes = 0;
            }
            tag.update({
                hours: tag.hours,
                minutes: tag.minutes,
                seconds: ++tag.seconds
            });
        }

        timer(e) {
            if (tag.timerState === 'Start') {
                tag.timerState = 'Stop';
                interval = setInterval(tag.tick, 1000);
            } else {
                tag.timerState = 'Start';
                clearInterval(interval);
                tag.timerDuration = tag.pad(tag.hours) + ':' + tag.pad(tag.minutes) + ':' + tag.pad(tag.seconds);
                tag.hours = 0;
                tag.minutes = 0;
                tag.seconds = 0;
            }
        }

        getEntries(url) {
            let entries = fetch(url || entriesApiUrl, {
                credentials: 'include',
                headers: new Headers({
                    'content-type': 'application/json',
                })
            }).then(function(response) {
                return response.json();
            })

            let users = fetch(usersApiUrl, {
                credentials: 'include',
                headers: new Headers({
                    'content-type': 'application/json',
                })
            }).then(function(response) {
                return response.json();
            })

            let tasks = fetch(tasksApiUrl, {
                credentials: 'include',
                headers: new Headers({
                    'content-type': 'application/json',
                })
            }).then(function(response) {
                return response.json();
            })

            Promise.all([entries, users, tasks]).then(function(e) {
                loading = document.querySelector('.loading');
                entriesTable = document.querySelector('.entries-table');

                loading.classList.add('d-none');
                entriesTable.classList.remove('d-none');

                let totalSeconds = 0;
                for (var entry in e[0].results) {
                    totalSeconds += tag.getTimeInSeconds(e[0].results[entry].duration);
                }
				let hours = Math.floor(totalSeconds / 3600);
				totalSeconds %= 3600;
				let minutes = Math.floor(totalSeconds / 60);
				let seconds = totalSeconds % 60;
                totalTimeCalc = hours +':'+ ('0'+minutes).slice(-2) +':'+ ('0'+seconds).slice(-2)

                tag.update({
                    entries: e[0].results,
                    users: promote(userId, e[1].results),
                    tasks: e[2].results,
                    totalTime: totalTimeCalc,
                    next: e[0].next,
                    previous: e[0].previous
                });

                $('.date-input').pickadate({
                    format: 'yyyy-mm-dd',
                    onStart: function() {
                        this.set('select', new Date());
                    }
                });
				$('.user-select').chosen();
				$('.task-select').chosen();
            });
        }

        tag.getEntries();

        entriesPage(e) {
            loading.classList.remove('d-none');
            entriesTable.classList.add('d-none');
            tag.getEntries(e.currentTarget.getAttribute('data-url'));
        }

        deleteEntry(e) {
            let csrfToken = Cookies.get('csrftoken');
            fetch(e.currentTarget.getAttribute('data-url'), {
                credentials: 'include',
                headers: new Headers({
                    'content-type': 'application/json',
                    'X-CSRFToken': csrfToken
                }),
                method: 'delete'
            }).then(function(response) {
                tag.getEntries();
            });
        }

        submitEntry(e) {
            e.preventDefault();
            let csrfToken = Cookies.get('csrftoken');
            let formValues = {
                date: this.refs.date.value,
                user: this.refs.user.value,
                duration: this.refs.duration.value,
                note: this.refs.note.value,
                task: this.refs.task.value
            }
            fetch(entriesApiUrl, {
                credentials: 'include',
                headers: new Headers({
                    'content-type': 'application/json',
                    'X-CSRFToken': csrfToken
                }),
                method: 'post',
                body: JSON.stringify(formValues)
            }).then(function(response) {
                tag.getEntries();
            });
        }
    </script>
</entries>
