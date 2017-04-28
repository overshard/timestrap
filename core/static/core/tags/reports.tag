<reports>
    <form class="mb-4 row" onsubmit={ getReport }>
        <div class="col-sm-6">
            <div class="form-group">
                <select class="user-select" ref="user">
                    <option value=''>User</option>
                    <option each={ users } value={ id }>{ username }</option>
                </select>
            </div>
            <div class="form-group">
                <select class="project-select" ref="project">
                    <option value=''>Project</option>
                    <option each={ projects } value={ id }>{ name } ({ client_details.name })</option>
                </select>
            </div>
            <div class="form-group">
                <select class="client-select" ref="client">
                    <option value=''>Client</option>
                    <option each={ clients } value={ id }>{ name }</option>
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
            <button type="submit" class="btn btn-primary btn-sm w-100">Generate Report</button>
        </div>
    </form>

    <p class="mb-4 clearfix">
        <button class="btn btn-primary btn-sm" onclick={ exportReport }>
            Export Report
        </button>

        <select class="custom-select form-control-sm" ref="export_format">
            <option value="csv">csv</option>
            <option value="xls">xls</option>
            <option value="xlsx">xlsx</option>
            <option value="tsv">tsv</option>
            <option value="ods">ods</option>
            <option value="json">json</option>
            <option value="yaml">yaml</option>
            <option value="html">html</option>
        </select>

        <pager update="{ getEntries }" />
    </p>

    <table class="reports-table table table-striped table-sm w-100 d-none">
        <thead class="thead-inverse">
            <tr>
                <th>Date</th>
                <th>User</th>
                <th>Duration</th>
                <th>Client, Project, and Note</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            <tr each={ entries }>
                <td>{ date }</td>
                <td>{ user_details.username }</td>
                <td>{ duration }</td>
                <td>
                    <span class="badge badge-success">{ project_details.client_details.name }</span>
                    <span class="badge badge-info">{ project_details.name }</span>
                    <br>
                    { note }
                </td>
                <td class="text-right"></td>
            </tr>
            <tr class="table-active">
                <td></td>
                <td>
                    Subtotal<br>
                    <strong>Total</strong>
                </td>
                <td>
                    { subtotalTime }<br>
                    <strong>{ totalTime }</strong>
                </td>
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
                    totalTime: data.total_duration,
                    subtotalTime: data.subtotal_duration,
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
                project: self.refs.project.value,
                project__client: self.refs.client.value,
                min_date: self.refs.min_date.value,
                max_date: self.refs.max_date.value
            }
            url = entriesApiUrl + '?' + $.param(query);
            self.getEntries(url);
        }


        exportReport(e) {
            query = {
                user: self.refs.user.value,
                project: self.refs.project.value,
                project__client: self.refs.client.value,
                min_date: self.refs.min_date.value,
                max_date: self.refs.max_date.value,
                export_format: self.refs.export_format.value
            }
            document.location.href = reportsExportUrl + '?' + $.param(query);
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

            quickFetch(projectsApiUrl).then(function(data) {
                self.update({projects: data.results});
                $('.project-select').chosen({width: '100%'});
            });

            quickFetch(clientsApiUrl).then(function(data) {
                self.update({clients: data.results});
                $('.client-select').chosen({width: '100%'});
            });

            $('.date-input').pickadate({
                format: 'yyyy-mm-dd'
            });
        });
    </script>
</reports>
