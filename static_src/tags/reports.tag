<reports>
    <div class="row py-2 mb-4 bg-faded rounded">
        <div class="col-12">
            <button id="export-report" class="btn btn-primary btn-sm" onclick={ exportReport }>
                <i class="fa fa-download" aria-hidden="true"></i>
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

            <pager update={ getEntries } />
        </div>
    </div>

    <form name="report-filters"
          class="row mb-4 pt-3 pb-1 bg-faded rounded"
          onsubmit={ getReport }>
        <div class="col-sm-6">
            <div class="form-group">
                <select id="report-filter-user" ref="user">
                    <option><!-- For select2 placeholder to work --></option>
                    <option each={ users } value={ id }>{ username }</option>
                </select>
            </div>
            <div class="form-group">
                <select id="report-filter-project" ref="project">
                    <option><!-- For select2 placeholder to work --></option>
                    <optgroup each={ c in clients } label={ c.name }>
                        <option each={ p in c.projects } value={ p.id }>
                            { p.name }
                        </option>
                    </optgroup>
                </select>
            </div>
            <div class="form-group">
                <select id="report-filter-client" ref="client">
                    <option><!-- For select2 placeholder to work --></option>
                    <option each={ clients } value={ id }>{ name }</option>
                </select>
            </div>
        </div>
        <div class="col-sm-6">
            <div class="form-group">
                <input id="report-filter-min-date"
                       type="text"
                       class="form-control form-control-sm date-input"
                       ref="min_date"
                       placeholder="Min Date"/>
            </div>
            <div class="form-group">
                <input id="report-filter-max-date"
                       type="text"
                       class="form-control form-control-sm date-input"
                       ref="max_date"
                       placeholder="Max Date"/>
            </div>
            <button id="generate-report" type="submit" class="btn btn-primary btn-sm w-100">
                Generate Report
            </button>
        </div>
    </form>

    <div class="entry-date-group mb-4" each={ dates }>
        <div class="row inset-row">
            <div class="col-12">
                <h2 class="display-4 text-muted">{ mainDate }</h5>
            </div>
        </div>
        <div class="entry-rows rounded">
            <div class="entry-row row py-2 bg-faded small" each={ entries } if={ mainDate === date }>
                <div class="col-sm-3 client-project">
                    <div class="text-muted small">
                        { project_details.client_details.name }
                    </div>
                    { project_details.name }
                </div>
                <div class="col-sm-5 d-flex align-self-end note">
                    { note }
                </div>
                <div class="col-sm-2 d-flex align-self-center justify-content-end display-4 duration">
                    { durationToString(duration) }
                </div>
                <div class="col-sm-2 d-flex align-self-end username">
                    { user_details.username }
                </div>
            </div>
        </div>
    </div>

    <div class="row bg-success text-white py-2 mb-4 rounded">
        <div class="offset-sm-6 col-sm-2 text-right">
            Subtotal<br>
            <strong>Total</strong>
        </div>
        <div class="col-sm-2 text-right">
            { durationToString(subtotalDuration) }<br>
            <strong>{ durationToString(totalDuration) }</strong>
        </div>
    </div>


    <script type="es6">
        this.getEntries = function(url) {
            url = (typeof url !== 'undefined') ? url : timestrapConfig.API_URLS.ENTRIES;
            toggleButtonBusy($('#generate-report'));
            toggleButtonBusy($('#export-report'));

            quickFetch(url).then(function(data) {
                let dates = [];
                let dateObjects = [];

                $.each(data.results, function(i, entry) {
                    entry.date = moment(entry.date).format('LL');
                    if ($.inArray(entry.date, dates) === -1) {
                        dates.push(entry.date);
                    }
                });
                $.each(dates, function(i, date) {
                    dateObjects.push({mainDate: date});
                });

                this.update({
                    dates: dateObjects,
                    entries: data.results,
                    totalDuration: data.total_duration,
                    subtotalDuration: data.subtotal_duration,
                    next: data.next,
                    previous: data.previous
                });

                toggleButtonBusy($('#generate-report'));
                toggleButtonBusy($('#export-report'));
            }.bind(this));
        }


        this.getReport = function(e) {
            e.preventDefault();
            query = {
                user: this.refs.user.value,
                project: this.refs.project.value,
                project__client: this.refs.client.value,
                min_date: this.refs.min_date.value,
                max_date: this.refs.max_date.value
            };
            url = timestrapConfig.API_URLS.ENTRIES + '?' + $.param(query);
            this.getEntries(url);
        }


        this.exportReport = function(e) {
            toggleButtonBusy($('#generate-report'));
            toggleButtonBusy($('#export-report'));
            query = {
                user: this.refs.user.value,
                project: this.refs.project.value,
                project__client: this.refs.client.value,
                min_date: this.refs.min_date.value,
                max_date: this.refs.max_date.value,
                export_format: this.refs.export_format.value
            };

            // TODO: Use a promise? This doesn't work for button toggling.
            document.location.href = timestrapConfig.CORE_URLS.REPORTS_EXPORT + '?' + $.param(query);
            toggleButtonBusy($('#generate-report'));
            toggleButtonBusy($('#export-report'));
        }


        this.on('mount', function() {
            this.getEntries();

            users = quickFetch(timestrapConfig.API_URLS.USERS);
            clients = quickFetch(timestrapConfig.API_URLS.CLIENTS);

            Promise.all([users, clients]).then(function(data) {
                this.update({
                    users: data[0].results,
                    clients: data[1].results,
                });
                $('#report-filter-user').select2({
                    placeholder: 'User',
                    width: '100%',
                    allowClear: true
                });
                $('#report-filter-client').select2({
                    placeholder: 'Client',
                    width: '100%',
                    allowClear: true
                });
                $('#report-filter-project').select2({
                    placeholder: 'Project',
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
