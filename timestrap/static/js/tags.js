riot.tag2('client', '<div class="row py-2 bg-faded rounded"> <virtual if="{edit && perms.change_client}"> <div class="col-10"> <input name="client-name" type="text" class="form-control form-control-sm" ref="name" riot-value="{name}"> </div> <div class="col-2"> <button name="client-save" class="btn btn-success btn-sm w-100" onclick="{saveClient}"> Save </button> </div> </virtual> <virtual if="{!edit}"> <div class="col-6 d-flex align-items-center"> <a class="client-view-projects text-primary font-weight-bold" onclick="{showProjects}" if="{perms.view_project}"> <i class="fa fa-chevron-circle-{chevron} small mr-2" aria-hidden="true"></i> <span class="mb-1">{name}</span> </a> <span class="text-primary font-weight-bold" if="{!perms.view_project}">{name}</span> </div> <div class="col-2 d-flex align-items-center"> <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i> <span class="mb-1">{total_duration}</span> </div> <div class="col-2 d-flex align-items-center"> <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i> <span class="mb-1">{total_projects}</span> </div> <div class="col-2"> <button name="client-change" class="btn btn-warning btn-sm w-100" onclick="{editClient}" disabled="{!perms.change_client}"> Edit </button> </div> </virtual> </div> <form name="project-add" onsubmit="{submitProject}" if="{productsShown && perms.add_project}"> <div class="row bg-faded py-2"> <div class="col-8"> <input name="project-name" type="text" class="form-control form-control-sm" ref="project_name" placeholder="New Project Name" required> </div> <div class="col-2"> <input name="project-estimate" type="text" class="form-control form-control-sm" placeholder="Estimate" ref="estimate" riot-value="{estimate}"> </div> <div class="col-2"> <button name="project-add-submit" type="submit" class="btn btn-success btn-sm w-100"> Add </button> </div> </div> </form> <div class="mb-2 project-rows"> <project class="row py-1 bg-faded" each="{projects}" data-is="project" if="{productsShown && perms.view_project}" perms="{perms}"></project> </div>', '', '', function(opts) {
this.editClient = function (e) {
    this.edit = true;
    this.update();
};

this.showProjects = function (e) {
    this.productsShown = !this.productsShown;
    if (this.chevron === 'down') {
        this.chevron = 'up';
    } else {
        this.chevron = 'down';
    }
    this.update();
};

this.saveClient = function (e) {
    e.preventDefault();
    clickedButton = e.target;
    toggleButtonBusy(clickedButton);
    let body = {
        name: this.refs.name.value
    };
    quickFetch(this.url, 'put', body).then(function (data) {
        if (data.id) {
            this.name = body.name;
        }
        this.name.value = '';
        this.edit = false;
        this.update();
        toggleButtonBusy(clickedButton);
    }.bind(this));
};

this.submitProject = function (e) {
    e.preventDefault();
    clickedButton = e.target;
    toggleButtonBusy(clickedButton);
    let body = {
        name: this.refs.project_name.value,
        estimate: this.refs.estimate.value,
        client: this.url
    };
    quickFetch(timestrapConfig.API_URLS.PROJECTS, 'post', body).then(function (data) {
        this.refs.project_name.value = '';
        if (data.id) {
            this.projects.unshift(data);
            this.update();
        }
        toggleButtonBusy(clickedButton);
    }.bind(this));
};

this.on('mount', function () {
    this.chevron = 'down';
    this.update();
}.bind(this));
});

riot.tag2('clients', '<div class="mb-4 clearfix"> <pager update="{getClients}"></pager> </div> <div class="row py-1 bg-inverse text-white font-weight-bold rounded-top"> <div class="col-sm-6"> Client </div> <div class="col-sm-2"> Total Time </div> <div class="col-sm-2"> # Related </div> <div class="col-sm-2"> </div> </div> <form name="client-add" class="row mb-4 py-2 bg-faded rounded-bottom" onsubmit="{submitClient}" if="{perms && perms.add_client}"> <div class="col-10"> <input name="client-name" type="text" class="form-control form-control-sm" ref="name" placeholder="New Client Name" required> </div> <div class="col-2"> <button name="client-add-submit" type="submit" class="btn btn-success btn-sm w-100"> Add </button> </div> </form> <client each="{clients}" perms="{perms}"></client>', '', '', function(opts) {
this.getClients = function (url) {
    url = typeof url !== 'undefined' ? url : timestrapConfig.API_URLS.CLIENTS;
    quickFetch(url).then(function (data) {
        this.update({
            clients: data.results,
            next: data.next,
            previous: data.previous
        });
    }.bind(this));
};

this.submitClient = function (e) {
    e.preventDefault();
    toggleButtonBusy(e.target);
    let body = {
        name: this.refs.name.value
    };
    quickFetch(timestrapConfig.API_URLS.CLIENTS, 'post', body).then(function (data) {
        this.refs.name.value = '';
        if (data.id) {
            this.clients.unshift(data);
            this.update();
        }
        toggleButtonBusy(e.target);
    }.bind(this));
};

this.getPerms = function () {
    quickFetch('/api/permissions/').then(function (data) {
        let perms = Object;
        $.each(data.results, function (i, perm) {
            perms[perm.codename] = perm;
        });
        this.perms = perms;
    });
};

this.on('mount', function () {
    this.getPerms();
    this.getClients();
}.bind(this));
});

riot.tag2('entries', '<div class="row py-2 mb-4 bg-faded rounded"> <div class="col-12"> <a href="/reports/" class="btn btn-primary btn-sm"> <i class="fa fa-book" aria-hidden="true"></i> Create Reports </a> <pager update="{getEntries}"></pager> </div> </div> <div class="row py-1 bg-inverse text-white font-weight-bold rounded-top"> <div class="col-sm-2"> Date </div> <div class="col-sm-2"> Project </div> <div class="col-sm-4"> Note </div> <div class="col-sm-2"> Duration </div> <div class="col-sm-2"> </div> </div> <form name="entry-add" class="row mb-4 py-2 bg-faded rounded-bottom" onsubmit="{submitEntry}" if="{perms && perms.add_entry}"> <div class="col-sm-2"> <input name="entry-date" type="text" class="form-control form-control-sm date-input" ref="date" placeholder="Date"> </div> <div class="col-sm-2"> <select name="entry-project" class="custom-select" ref="project" required> <option></option> <optgroup each="{c in clients}" label="{c}"> <option each="{projects}" riot-value="{url}" if="{c === client_details.name}"> {name} </option> </optgroup> </select> </div> <div class="col-sm-4"> <input name="entry-note" type="text" class="form-control form-control-sm" ref="note" placeholder="Note"> </div> <div class="col-sm-2"> <input name="entry-duration" type="text" class="form-control form-control-sm text-right font-weight-bold" oninput="{timer}" ref="duration" placeholder="0:00" riot-value="{timerDuration}" required> </div> <div class="col-sm-2"> <button name="entry-add-submit" type="submit" class="btn btn-success btn-sm w-100" onclick="{timer}"> {timerState} </button> </div> </form> <div class="mb-4" each="{d in dates}"> <div class="row inset-row"> <div class="col-12"> <h2 class="display-4 text-muted">{moment(d).format(\'LL\')}</h5> </div> </div> <div class="entry-rows rounded"> <entry each="{entries}" if="{d === date}" class="row py-2 bg-faded small" perms="{perms}"></entry> </div> </div> <div class="row bg-success text-white py-2 mb-4 rounded"> <div class="offset-sm-6 col-sm-2 text-right"> Subtotal<br> <strong>Total</strong> </div> <div class="col-sm-2 text-right"> {durationToString(subtotalDuration)}<br> <strong>{durationToString(totalDuration)}</strong> </div> </div>', '', '', function(opts) {
this.tick = function (entry) {
    ++entry.totalSeconds;
    let hours = pad(Math.floor(entry.totalSeconds / 3600));
    let minutes = pad(Math.floor(entry.totalSeconds % 3600 / 60));
    let seconds = pad(entry.totalSeconds % 3600 % 60);
    entry.update({
        timerDuration: hours + ':' + minutes + ':' + seconds
    });
};

this.timer = function (e) {
    let duration = this.refs.duration.value;
    if (this.timerState === 'Start' && duration) {
        this.timerState = 'Add';
    } else if (this.timerState === 'Start') {
        this.timerState = 'Stop';
        this.timerDuration = '00:00:00';
        this.totalSeconds = 0;
        interval = setInterval(this.tick, 1000, this);
        e.preventDefault();
    } else if (this.timerState === 'Stop') {
        this.timerState = 'Add';
        this.totalSeconds = 0;
        clearInterval(interval);
        let dur = this.timerDuration;
        this.timerDuration = dur.substr(0, dur.lastIndexOf(':'));
        this.totalSeconds = 0;
        e.preventDefault();
    } else if (!duration) {
        this.timerState = 'Start';
        e.preventDefault();
    }
};

this.getEntries = function (url) {
    let userEntries = timestrapConfig.API_URLS.ENTRIES + '?user=' + timestrapConfig.USER.ID;
    url = typeof url !== 'undefined' ? url : userEntries;

    let entries = quickFetch(url);
    let projects = quickFetch(timestrapConfig.API_URLS.PROJECTS);

    Promise.all([entries, projects]).then(function (e) {
        let dates = [];
        $.each(e[0].results, function (i, entry) {
            if ($.inArray(entry.date, dates) === -1) {
                dates.push(entry.date);
            }
        });

        let clients = [];
        $.each(e[1].results, function (i, project) {
            if ($.inArray(project.client_details.name, clients) === -1) {
                clients.push(project.client_details.name);
            }
        });

        this.update({
            dates: dates,
            clients: clients,
            entries: e[0].results,
            projects: e[1].results,
            totalDuration: e[0].total_duration,
            subtotalDuration: e[0].subtotal_duration,
            next: e[0].next,
            previous: e[0].previous
        });

        $('.custom-select').select2({
            placeholder: 'Project',
            width: '100%',
            dropdownAutoWidth: true
        });

        $('.date-input').pickadate({
            format: 'yyyy-mm-dd',
            onStart: function () {
                this.set('select', new Date());
            }
        });
    }.bind(this));
};

this.submitEntry = function (e) {
    e.preventDefault();
    clickedButton = e.target;
    toggleButtonBusy(clickedButton);
    let body = {
        user: timestrapConfig.USER.URL,
        duration: this.refs.duration.value,
        note: this.refs.note.value,
        project: this.refs.project.value,
        date: this.refs.date.value
    };
    quickFetch(timestrapConfig.API_URLS.ENTRIES, 'post', body).then(function (data) {
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
};

this.updateTotals = function (newDuration, oldDuration) {
    this.totalDuration += newDuration - oldDuration;
    this.subtotalDuration += newDuration - oldDuration;
    this.update();
};

this.getPerms = function () {
    quickFetch('/api/permissions/').then(function (data) {
        let perms = Object;
        $.each(data.results, function (i, perm) {
            perms[perm.codename] = perm;
        });
        this.perms = perms;
    });
};

this.on('mount', function () {
    this.timerState = 'Start';
    this.getPerms();
    this.getEntries();
}.bind(this));
});

riot.tag2('entry', '<virtual if="{!edit}"> <div class="col-sm-3 client-project"> <div class="text-muted small"> {project_details.client_details.name} </div> {project_details.name} </div> <div class="col-sm-5 d-flex align-self-end note"> {note} </div> <virtual if="{!runTimer}"> <div class="col-sm-2 d-flex align-self-center justify-content-end display-4 duration"> {durationToString(duration)} </div> <div class="col-sm-2 d-flex align-self-center justify-content-end"> <virtual if="{perms.change_entry || perms.delete_entry}"> <button name="entry-menu" class="btn btn-faded btn-sm btn-icon dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> <i class="fa fa-ellipsis-v" aria-hidden="true"></i> </button> <div class="dropdown-menu dropdown-menu-right" aria-labelledby="entry-menu"> <a class="dropdown-item entry-menu-restart" href="#" onclick="{restartEntry}" if="{perms.change_entry}"> Restart </a> <a class="dropdown-item entry-menu-change" href="#" onclick="{editEntry}" if="{perms.change_entry}"> Edit </a> <a class="dropdown-item entry-menu-delete" href="#" onclick="{deleteEntry}" if="{perms.delete_entry}"> Delete </a> </div> </virtual> </div> </virtual> <virtual if="{runTimer}"> <div class="col-sm-2"> <input name="entry-duration" type="text" class="form-control form-control-sm text-right font-weight-bold" ref="duration" placeholder="0:00" riot-value="{timerDuration}"> </div> <div class="col-sm-2"> <button name="entry-save" type="submit" class="btn btn-success btn-sm w-100" onclick="{timer}"> {timerState} </div> </button> </virtual> </virtual> <virtual if="{edit}"> <div class="col-sm-3"> <select name="entry-project" class="custom-select custom-select-edit" ref="project" required> <optgroup each="{c in parent.clients}" label="{c}"> <option each="{p in parent.parent.projects}" riot-value="{p.url}" if="{c === p.client_details.name}" selected="{p.id === parent.project_details.id}"> {p.name} </option> </optgroup> </select> </div> <div class="col-sm-5"> <input name="entry-note" type="text" class="form-control form-control-sm" ref="note" placeholder="Note" riot-value="{note}"> </div> <div class="col-sm-2"> <input name="entry-duration" type="text" class="form-control form-control-sm text-right font-weight-bold" ref="duration" placeholder="0:00" riot-value="{durationToString(duration)}"> </div> <div class="col-sm-2"> <button name="entry-save" class="btn btn-success btn-sm w-100" onclick="{saveEntry}"> Save </button> </div> </virtual>', '', '', function(opts) {
this.editEntry = function (e) {
    e.preventDefault();
    this.edit = true;
    this.update();
    $('.custom-select-edit').select2({
        width: '100%',
        dropdownAutoWidth: true
    });
};

this.restartEntry = function (e) {
    this.runTimer = true;
    this.timer(e);
};

this.timer = function (e) {
    if (!this.timerState) {
        this.timerState = 'Stop';
        let hours = Math.floor(this.duration);
        let minutes = (this.duration - hours) * 60;
        this.totalSeconds = hours * 3600 + minutes * 60;
        this.parent.tick(this);
        interval = setInterval(this.parent.tick, 1000, this);
        e.preventDefault();
    } else {
        this.timerState = undefined;
        clearInterval(interval);
        let dur = this.timerDuration;
        this.runTimer = false;
        this.edit = true;
        this.update();
        this.refs.duration.value = dur.substr(0, dur.lastIndexOf(':'));
        e.preventDefault();
    }
};

this.saveEntry = function (e) {
    e.preventDefault();
    clickedButton = e.target;
    toggleButtonBusy(clickedButton);
    let body = {
        user: this.user,
        project: this.refs.project.value,
        note: this.refs.note.value,
        duration: this.refs.duration.value
    };
    quickFetch(this.url, 'put', body).then(function (data) {
        this.note.value = '';
        this.duration.value = '';
        this.project.value = '';
        this.edit = false;
        if (data.id) {
            let index = this.parent.entries.indexOf(e.item);
            this.parent.entries[index] = data;
            this.project = data.project;
            this.note = data.note;
            let oldDuration = this.duration;
            this.duration = data.duration;
            this.update();
            this.parent.updateTotals(this.duration, oldDuration);
        } else {
            this.update();
        }
        toggleButtonBusy(clickedButton);
    }.bind(this));
};

this.deleteEntry = function (e) {
    e.preventDefault();
    quickFetch(this.url, 'delete').then(function (response) {
        if (response.status === 204) {
            let index = this.parent.entries.indexOf(e.item);
            this.parent.entries.splice(index, 1);
            // updateTotals executes parent update.
            this.parent.updateTotals(0, this.duration);
        }
    }.bind(this));
};
});

riot.tag2('pager', '<button class="btn btn-primary btn-sm pull-right" data-url="{this.parent.next}" if="{this.parent.next}" onclick="{loadDataUrl}"> Next <i class="fa fa-arrow-right" aria-hidden="true"></i> </button> <button class="btn btn-primary btn-sm pull-right mr-1" data-url="{this.parent.previous}" if="{this.parent.previous}" onclick="{loadDataUrl}"> <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous </button>', '', '', function(opts) {
this.loadDataUrl = function (e) {
    this.opts.update(e.currentTarget.getAttribute('data-url'));
};
});

riot.tag2('project', '<virtual if="{edit}"> <div class="col-8"> <input name="project-name" type="text" class="form-control form-control-sm" ref="name" riot-value="{name}"> </div> <div class="col-2"> <input name="project-estimate" type="text" class="form-control form-control-sm" placeholder="Estimate" ref="estimate" riot-value="{estimate}"> </div> <div class="col-2"> <button name="project-save" class="btn btn-success btn-sm w-100" onclick="{saveProject}"> Save </button> </div> </virtual> <virtual if="{!edit}"> <div class="mb-1 col-6">{name}</div> <virtual if="{percent_done}"> <div class="col-4 d-flex align-items-center"> <div class="progress w-100"> <virtual if="{percent_done > 100}"> <div class="progress-bar bg-danger" riot-style="width: {percent_done}%"> {percent_done}% </div> </virtual> <virtual if="{percent_done <= 100}"> <div class="progress-bar" riot-style="width: {percent_done}%"> {percent_done}% </div> </virtual> </div> </div> </virtual> <virtual if="{!percent_done}"> <div class="col-2 d-flex align-items-center"> <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i> <span class="mb-1">{total_duration}</span> </div> <div class="col-2 d-flex align-items-center"> <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i> <span class="mb-1">{total_entries}</span> </div> </virtual> <div class="col-2"> <button name="project-change" class="btn btn-warning btn-sm w-100" onclick="{editProject}" disabled="{!perms.change_project}"> Edit </button> </div> </virtual>', '', '', function(opts) {
this.editProject = function (e) {
    this.edit = true;
    this.update();
};

this.saveProject = function (e) {
    e.preventDefault();
    clickedButton = e.target;
    toggleButtonBusy(clickedButton);
    let body = {
        client: this.client,
        name: this.refs.name.value,
        estimate: this.refs.estimate.value
    };
    quickFetch(this.url, 'put', body).then(function (data) {
        if (data.id) {
            this.name = data.name;
            this.estimate = data.estimate;
            this.percent_done = data.percent_done;
        }
        this.name.value = '';
        this.edit = false;
        this.update();
        toggleButtonBusy(clickedButton);
    }.bind(this));
};
});

riot.tag2('reports', '<div class="row py-2 mb-4 bg-faded rounded"> <div class="col-12"> <button id="export-report" class="btn btn-primary btn-sm" onclick="{exportReport}"> <i class="fa fa-download" aria-hidden="true"></i> Export Report </button> <select class="custom-select form-control-sm" ref="export_format"> <option value="csv">csv</option> <option value="xls">xls</option> <option value="xlsx">xlsx</option> <option value="tsv">tsv</option> <option value="ods">ods</option> <option value="json">json</option> <option value="yaml">yaml</option> <option value="html">html</option> </select> <pager update="{getEntries}"></pager> </div> </div> <form name="report-filters" class="row mb-4 pt-3 pb-1 bg-faded rounded" onsubmit="{getReport}"> <div class="col-sm-6"> <div class="form-group"> <select id="report-filter-user" class="user-select" ref="user"> <option></option> <option each="{users}" riot-value="{id}">{username}</option> </select> </div> <div class="form-group"> <select id="report-filter-project" class="project-select" ref="project"> <option></option> <optgroup each="{c in clients}" label="{c}"> <option each="{projects}" riot-value="{id}" if="{c === client_details.name}"> {name} </option> </optgroup> </select> </div> <div class="form-group"> <select id="report-filter-client" class="client-select" ref="client"> <option></option> <option each="{clients}" riot-value="{id}">{name}</option> </select> </div> </div> <div class="col-sm-6"> <div class="form-group"> <input id="report-filter-min-date" type="text" class="form-control form-control-sm date-input" ref="min_date" placeholder="Min Date"> </div> <div class="form-group"> <input id="report-filter-max-date" type="text" class="form-control form-control-sm date-input" ref="max_date" placeholder="Max Date"> </div> <button id="generate-report" type="submit" class="btn btn-primary btn-sm w-100"> Generate Report </button> </div> </form> <div class="entry-date-group mb-4" each="{dates}"> <div class="row inset-row"> <div class="col-12"> <h2 class="display-4 text-muted">{mainDate}</h5> </div> </div> <div class="entry-rows rounded"> <div class="entry-row row py-2 bg-faded small" each="{entries}" if="{mainDate === date}"> <div class="col-sm-3 client-project"> <div class="text-muted small"> {project_details.client_details.name} </div> {project_details.name} </div> <div class="col-sm-5 d-flex align-self-end note"> {note} </div> <div class="col-sm-2 d-flex align-self-center justify-content-end display-4 duration"> {durationToString(duration)} </div> <div class="col-sm-2 d-flex align-self-end username"> {user_details.username} </div> </div> </div> </div> <div class="row bg-success text-white py-2 mb-4 rounded"> <div class="offset-sm-6 col-sm-2 text-right"> Subtotal<br> <strong>Total</strong> </div> <div class="col-sm-2 text-right"> {durationToString(subtotalDuration)}<br> <strong>{durationToString(totalDuration)}</strong> </div> </div>', '', '', function(opts) {
this.getEntries = function (url) {
    url = typeof url !== 'undefined' ? url : timestrapConfig.API_URLS.ENTRIES;
    toggleButtonBusy($('#generate-report'));
    toggleButtonBusy($('#export-report'));

    quickFetch(url).then(function (data) {
        let dates = [];
        let dateObjects = [];

        $.each(data.results, function (i, entry) {
            entry.date = moment(entry.date).format('LL');
            if ($.inArray(entry.date, dates) === -1) {
                dates.push(entry.date);
            }
        });
        $.each(dates, function (i, date) {
            dateObjects.push({ mainDate: date });
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
};

this.getReport = function (e) {
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
};

this.exportReport = function (e) {
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
};

this.on('mount', function () {
    this.getEntries();

    quickFetch(timestrapConfig.API_URLS.USERS).then(function (data) {
        this.update({ users: data.results });
        $('.user-select').select2({
            placeholder: 'User',
            width: '100%',
            allowClear: true
        });
    }.bind(this));

    quickFetch(timestrapConfig.API_URLS.PROJECTS).then(function (data) {
        let clients = [];
        $.each(data.results, function (i, project) {
            if ($.inArray(project.client_details.name, clients) === -1) {
                clients.push(project.client_details.name);
            }
        });

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

    quickFetch(timestrapConfig.API_URLS.CLIENTS).then(function (data) {
        this.update({ clients: data.results });
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
});
