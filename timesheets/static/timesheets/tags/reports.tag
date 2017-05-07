<reports>
    <form class="mb-4 row report-form shadow-muted pt-3 pb-1" onsubmit={ getReport }>
        <div class="col-sm-6">
            <div class="form-group">
                <select class="user-select" ref="user">
                    <option><!-- For select2 placeholder to work --></option>
                    <option each={ users } value={ id }>{ username }</option>
                </select>
            </div>
            <div class="form-group">
                <select class="project-select" ref="project">
                    <option><!-- For select2 placeholder to work --></option>
                    <optgroup each={ c in clients } label={ c.name }>
                        <option each={ projects }
                                value={ url }
                                if={ c.name === client_details.name }>
                            { name }
                        </option>
                    </optgroup>
                </select>
            </div>
            <div class="form-group">
                <select class="client-select" ref="client">
                    <option><!-- For select2 placeholder to work --></option>
                    <option each={ clients } value={ id }>{ name }</option>
                </select>
            </div>
        </div>
        <div class="col-sm-6">
            <div class="form-group">
                <input type="text"
                       class="form-control form-control-sm date-input"
                       ref="min_date"
                       placeholder="Min Date"/>
            </div>
            <div class="form-group">
                <input type="text"
                       class="form-control form-control-sm date-input"
                       ref="max_date"
                       placeholder="Max Date"/>
            </div>
            <button type="submit" class="btn btn-primary btn-sm w-100">
                Generate Report
            </button>
        </div>
    </form>

    <p class="mb-4 clearfix">
        <button class="btn btn-primary btn-sm rounded-0" onclick={ exportReport }>
            Export Report
        </button>

        <select class="custom-select form-control-sm rounded-0" ref="export_format">
            <option value="csv">csv</option>
            <option value="xls">xls</option>
            <option value="xlsx">xlsx</option>
            <option value="tsv">tsv</option>
            <option value="ods">ods</option>
            <option value="json">json</option>
            <option value="yaml">yaml</option>
            <option value="html">html</option>
        </select>

        <pager update={ getEntries } />
    </p>

    <div class="mb-5" each={ dates }>
        <h5 class="text-muted">{ mainDate }</h5>
        <div class="entry-rows">
            <div class="row py-2 bg-faded small" each={ entries } if={ mainDate === date }>
                <div class="col-sm-3">
                    <div class="text-muted small">
                        { project_details.client_details.name }
                    </div>
                    { project_details.name }
                </div>
                <div class="col-sm-5 d-flex align-self-center">
                    { note }
                </div>
                <div class="col-sm-2 d-flex align-self-center justify-content-end font-weight-bold">
                    { durationToString(duration) }
                </div>
                <div class="col-sm-2 d-flex align-self-center">
                    { user_details.username }
                </div>
            </div>
        </div>
    </div>


    <script>
        getEntries(url) {
            url = (typeof url !== 'undefined') ? url : entriesApiUrl;

            quickFetch(url).then(function(data) {
                let dates = [];
                let dateObjects = [];

                $.each(data.results, function(i, entry) {
                    if ($.inArray(entry.date, dates) === -1) {
                        dates.push(entry.date);
                    }
                })
                $.each(dates, function(i, date) {
                    dateObjects.push({mainDate: date});
                })

                this.update({
                    dates: dateObjects,
                    entries: data.results,
                    totalDuration: data.total_duration,
                    subtotalDuration: data.subtotal_duration,
                    next: data.next,
                    previous: data.previous
                });
            }.bind(this));
        }


        getReport(e) {
            e.preventDefault();
            query = {
                user: this.refs.user.value,
                project: this.refs.project.value,
                project__client: this.refs.client.value,
                min_date: this.refs.min_date.value,
                max_date: this.refs.max_date.value
            }
            url = entriesApiUrl + '?' + $.param(query);
            this.getEntries(url);
        }


        exportReport(e) {
            query = {
                user: this.refs.user.value,
                project: this.refs.project.value,
                project__client: this.refs.client.value,
                min_date: this.refs.min_date.value,
                max_date: this.refs.max_date.value,
                export_format: this.refs.export_format.value
            }
            document.location.href = reportsExportUrl + '?' + $.param(query);
        }


        reportsPage(e) {
            this.getEntries(e.currentTarget.getAttribute('data-url'));
        }


        this.on('mount', function() {
            this.getEntries();

            quickFetch(usersApiUrl).then(function(data) {
                this.update({users: data.results});
                $('.user-select').select2({
                    placeholder: 'User',
                    width: '100%',
                    allowClear: true
                });
            }.bind(this));

            quickFetch(projectsApiUrl).then(function(data) {
                let clients = [];
                $.each(data.results, function(i, project) {
                    if ($.inArray(project.client_details.name, clients) === -1) {
                        clients.push(project.client_details.name);
                    }
                })

                this.update({
                    clients: clients,
                    projects: data.results
                });
                $('.project-select').select2({
                    placeholder: 'Project',
                    width: '100%',
                    allowClear: true
                });
            }.bind(this));

            quickFetch(clientsApiUrl).then(function(data) {
                this.update({clients: data.results});
                $('.client-select').select2({
                    placeholder: 'Client',
                    width: '100%',
                    allowClear: true
                });
            }.bind(this));

            $('.date-input').pickadate({
                format: 'yyyy-mm-dd'
            });
        }.bind(this));
    </script>
</reports>
