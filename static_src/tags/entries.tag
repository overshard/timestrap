<entries>
    <div class="row py-2 mb-4 bg-faded rounded">
        <div class="col-12">
            <a href="/reports/"
               class="btn btn-primary btn-sm">
                <i class="fa fa-book" aria-hidden="true"></i>
                Create Reports
            </a>

            <pager update={ getEntries }/>
        </div>
    </div>

    <div class="row py-1 bg-inverse text-white font-weight-bold rounded-top">
        <div class="col-sm-3 mb-2">
            Date
        </div>
        <div class="col-sm-3 mb-2">
            Task
        </div>
        <div class="col-sm-6">
        </div>
        <div class="col-sm-3">
            Project
        </div>
        <div class="col-sm-5">
            Note
        </div>
        <div class="col-sm-2">
            Duration
        </div>
        <div class="col-sm-2">
        </div>
    </div>

    <form name="entry-add"
          class="row mb-4 py-2 bg-faded rounded-bottom"
          onsubmit={ submitEntry }
          if={ perms && perms.add_entry }>
        <div class="col-sm-3 mb-2">
            <input name="entry-date"
                   type="text"
                   class="form-control form-control-sm date-input"
                   ref="date"
                   placeholder="Date" />
        </div>
        <div class="col-sm-3">
            <select name="entry-task" class="task-select" ref="task">
                <option><!-- For select2 placeholder to work --></option>
                <option each={ tasks }
                        value={ url }>
                    { name }
                </option>
            </select>
        </div>
        <div class="col-sm-6">
        </div>
        <div class="col-sm-3">
            <select name="entry-project" class="project-select" ref="project" required>
                <option><!-- For select2 placeholder to work --></option>
                <optgroup each={ c in clients } label={ c }>
                    <option each={ projects }
                            value={ url }
                            if={ c === client_details.name }>
                        { name }
                    </option>
                </optgroup>
            </select>
        </div>
        <div class="col-sm-5">
            <input name="entry-note"
                   type="text"
                   class="form-control form-control-sm"
                   ref="note"
                   placeholder="Note"/>
        </div>
        <div class="col-sm-2">
            <input name="entry-duration"
                   type="text"
                   class="form-control form-control-sm text-right font-weight-bold"
                   oninput={ timer }
                   ref="duration"
                   placeholder="0:00"
                   value={ timerDuration }
                   required />
        </div>
        <div class="col-sm-2">
            <button name="entry-add-submit"
                    type="submit"
                    class="btn btn-success btn-sm w-100"
                    onclick={ timer }>
                { timerState }
            </button>
        </div>
    </form>

    <div class="mb-4" each={ d in dates }>
        <div class="row inset-row">
            <div class="col-12">
                <h2 class="display-4 text-muted">{ moment(d).format('LL') }</h5>
            </div>
        </div>
        <div class="entry-rows rounded">
            <entry each={ entries }
                   if={ d === date }
                   class="row py-2 bg-faded small"
                   perms={ perms} />
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


    <style>
    </style>


    <script type="es6">
        tickTimer = function(entry) {
            ++entry.totalSeconds;
            let hours = pad(Math.floor(entry.totalSeconds / 3600));
            let minutes = pad(Math.floor(entry.totalSeconds % 3600 / 60));
            let seconds = pad(entry.totalSeconds % 3600 % 60);
            entry.update({
                timerDuration: hours + ':' + minutes + ':' + seconds
            });
        }.bind(this);


        timer = function(e) {
            let duration = this.refs.duration.value;
            if (this.timerState === 'Start' && duration) {
                this.timerState = 'Add';
            } else if (this.timerState === 'Start') {
                this.timerState = 'Stop';
                this.timerDuration = '00:00:00';
                this.totalSeconds = 0;
                this.interval = setInterval(tickTimer, 1000, this);
                e.preventDefault();
            } else if (this.timerState === 'Stop') {
                this.timerState = 'Add';
                this.totalSeconds = 0;
                clearInterval(this.interval);
                let dur = this.timerDuration;
                this.timerDuration = dur.substr(0, dur.lastIndexOf(':'));
                this.totalSeconds = 0;
                e.preventDefault();
            } else if (!duration) {
                this.timerState = 'Start';
                e.preventDefault();
            }
        }.bind(this);


        getEntries = function(url) {
            let userEntries = timestrapConfig.API_URLS.ENTRIES + '?user=' + timestrapConfig.USER.ID;
            url = (typeof url !== 'undefined') ? url : userEntries;

            let entries = quickFetch(url);
            let projects = quickFetch(timestrapConfig.API_URLS.PROJECTS);
            let tasks = quickFetch(timestrapConfig.API_URLS.TASKS);

            Promise.all([entries, projects, tasks]).then(function(e) {
                let dates = [];
                $.each(e[0].results, function(i, entry) {
                    if ($.inArray(entry.date, dates) === -1) {
                        dates.push(entry.date);
                    }
                });

                let clients = [];
                $.each(e[1].results, function(i, project) {
                    if ($.inArray(project.client_details.name, clients) === -1) {
                        clients.push(project.client_details.name);
                    }
                });

                this.update({
                    dates: dates,
                    clients: clients,
                    entries: e[0].results,
                    projects: e[1].results,
                    tasks: e[2].results,
                    totalDuration: e[0].total_duration,
                    subtotalDuration: e[0].subtotal_duration,
                    next: e[0].next,
                    previous: e[0].previous
                });

                $('.project-select').select2({
                    placeholder: 'Project',
                    width: '100%',
                    dropdownAutoWidth: true
                });

                $('.task-select').select2({
                    placeholder: 'Task',
                    width: '100%',
                    dropdownAutoWidth: true
                });

                $('.date-input').pickadate({
                    format: 'yyyy-mm-dd',
                    onStart: function() {
                        this.set('select', new Date());
                    }
                });
            }.bind(this));
        }.bind(this);


        submitEntry = function(e) {
            e.preventDefault();
            clickedButton = e.target;
            toggleButtonBusy(clickedButton);
            let body = {
                user: timestrapConfig.USER.URL,
                duration: this.refs.duration.value,
                note: this.refs.note.value,
                project: this.refs.project.value,
                task: this.refs.task.value,
                date: this.refs.date.value
            };
            quickFetch(timestrapConfig.API_URLS.ENTRIES, 'post', body).then(function(data) {
                this.refs.duration.value = '';
                this.refs.note.value = '';
                if (data.id) {
                    data.date = moment(data.date).format('LL');
                    this.entries.unshift(data);
                    if ($.inArray(data.date, this.dates) === -1) {
                        this.dates.unshift(data.date);
                    }
                    this.timerState = 'Start';
                    this.updateTotals(data.duration, 0);
                }
                toggleButtonBusy(clickedButton);
            }.bind(this));
        }.bind(this);


        updateTotals = function(newDuration, oldDuration) {
            this.totalDuration += newDuration - oldDuration;
            this.subtotalDuration += newDuration - oldDuration;
            this.update();
        }.bind(this);


        getPerms = function() {
            prefetch.PERMISSIONS.then(function(data) {
                let perms = Object;
                $.each(data.results, function(i, perm) {
                    perms[perm.codename] = perm;
                });
                this.perms = perms;
            });
        }.bind(this);


        this.on('mount', function() {
            this.timerState = 'Start';
            getPerms();
            getEntries();
        }.bind(this));
    </script>
</entries>
