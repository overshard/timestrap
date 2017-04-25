<reports>
    <p class="mb-4 clearfix">
        <button class="btn btn-primary btn-sm pull-right"
                data-url="{ next }"
                if={ next }
                onclick={ reportsPage }>
            Next <i class="fa fa-arrow-right" aria-hidden="true"></i>
        </button>

        <button class="btn btn-primary btn-sm pull-right mr-1"
                data-url="{ previous }"
                if={ previous }
                onclick={ reportsPage }>
            <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous
        </button>
    </p>

    <form class="mb-4 row" onsubmit={ getReport }>
        <div class="col-sm-6">
            <div class="form-group">
                <select class="user-select" ref="user">
                    <option value=''>User</option>
                    <option each={ users } value={ id }>{ username }</option>
                </select>
            </div>
            <div class="form-group">
                <select class="task-select" ref="task">
                    <option value=''>Task</option>
                    <option each={ tasks } value={ id }>{ name }</option>
                </select>
            </div>
            <div class="form-group">
                <select class="timesheet-select" ref="timesheet">
                    <option value=''>Timesheet</option>
                    <option each={ timesheets } value={ id }>{ name }</option>
                </select>
            </div>
        </div>
        <div class="col-sm-6">
            <div class="form-group">
                <input type="text" class="form-control form-control-sm date-input" ref="min_date" placeholder="Min Date">
            </div>
            <div class="form-group">
                <input type="text" class="form-control form-control-sm date-input" ref="max_date" placeholder="Max Date">
            </div>
            <button type="submit" class="btn btn-primary btn-sm">Get Report</button>
        </div>
    </form>

    <table class="reports-table table table-striped table-sm w-100 d-none">
        <thead class="thead-inverse">
            <tr>
                <th>Date</th>
                <th>User</th>
                <th>Duration</th>
                <th>Timesheet, Task, and Note</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            <tr each={ entries }>
                <td>{ date }</td>
                <td>{ user_details.username }</td>
                <td>{ duration }</td>
                <td>
                    <span class="badge badge-primary">{ task_details.timesheet_details.name }</span>
                    <span class="badge badge-info">{ task_details.name }</span>
                    <br>
                    { note }
                </td>
                <td class="text-right"></td>
            </tr>
            <tr class="table-active">
                <td></td>
                <td><strong>Total</strong></td>
                <td><strong>{ totalTime }</strong></td>
                <td></td>
                <td></td>
            </tr>
        </tbody>
    </table>

    <p class="loading text-center my-5">
        <i class="fa fa-spinner" aria-hidden="true"></i>
    </p>

    <script>
        var self = this;


        getEntries(url) {
            url = (typeof url !== 'undefined') ? url : entriesApiUrl;

            $('.loading, .reports-table').toggleClass('d-none');

            quickFetch(url).then(function(data) {
                self.update({
                    entries: data.results,
                    totalTime: getTotalTime(data.results),
                    next: data.next,
                    previous: data.previous
                });
                $('.loading, .reports-table').toggleClass('d-none');
            });
        }


        getReport(e) {
            e.preventDefault();
            query = {
                user: self.refs.user.value,
                task: self.refs.task.value,
                task__timesheet: self.refs.timesheet.value,
                min_date: self.refs.min_date.value,
                max_date: self.refs.max_date.value
            }
            url = entriesApiUrl + '?' + $.param(query);
            self.getEntries(url);
        }


        reportsPage(e) {
            self.getEntries(e.currentTarget.getAttribute('data-url'));
        }


        self.getEntries();

        self.on('mount', function() {
            quickFetch(usersApiUrl).then(function(data) {
                self.update({users: data.results});
                $('.user-select').chosen({width: '100%'});
            });

            quickFetch(tasksApiUrl).then(function(data) {
                self.update({tasks: data.results});
                $('.task-select').chosen({width: '100%'});
            });

            quickFetch(timesheetsApiUrl).then(function(data) {
                self.update({timesheets: data.results});
                $('.timesheet-select').chosen({width: '100%'});
            });

            $('.date-input').pickadate({
                format: 'yyyy-mm-dd'
            });
        });
    </script>
</reports>
