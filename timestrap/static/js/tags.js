riot.tag2('client', '<div class="row py-2 bg-faded rounded"> <virtual if="{edit && perms.change_client}"> <div class="col-10"> <input name="client-name" type="text" class="form-control form-control-sm" ref="name" riot-value="{name}"> </div> <div class="col-2"> <button name="client-save" class="btn btn-success btn-sm w-100" onclick="{saveClient}"> Save </button> </div> </virtual> <virtual if="{!edit}"> <div class="col-6 d-flex align-items-center"> <a class="client-view-projects text-primary font-weight-bold" onclick="{showProjects}" if="{perms.view_project}"> <i class="fa fa-chevron-circle-{chevron} small mr-2" aria-hidden="true"></i> <span class="mb-1">{name}</span> </a> <span class="text-primary font-weight-bold" if="{!perms.view_project}">{name}</span> </div> <div class="col-2 d-flex align-items-center"> <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i> <span class="mb-1">{total_duration}</span> </div> <div class="col-2 d-flex align-items-center"> <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i> <span class="mb-1">{total_projects}</span> </div> <div class="col-2"> <button name="client-change" class="btn btn-warning btn-sm w-100" onclick="{editClient}" disabled="{!perms.change_client}"> Edit </button> </div> </virtual> </div> <form name="project-add" onsubmit="{submitProject}" if="{productsShown && perms.add_project}"> <div class="row bg-faded py-2"> <div class="col-8"> <input name="project-name" type="text" class="form-control form-control-sm" ref="project_name" placeholder="New Project Name" required> </div> <div class="col-2"> <input name="project-estimate" type="text" class="form-control form-control-sm" placeholder="Estimate" ref="estimate" riot-value="{estimate}"> </div> <div class="col-2"> <button name="project-add-submit" type="submit" class="btn btn-success btn-sm w-100"> Add </button> </div> </div> </form> <div class="mb-2 project-rows"> <project class="row py-1 bg-faded" each="{projects}" data-is="project" if="{productsShown && perms.view_project}" perms="{perms}"></project> </div>', '', '', function(opts) {
editClient = function (e) {
    this.edit = true;
    this.update();
};

showProjects = function (e) {
    this.productsShown = !this.productsShown;
    if (this.chevron === 'down') {
        this.chevron = 'up';
    } else {
        this.chevron = 'down';
    }
    this.update();
};

saveClient = function (e) {
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

submitProject = function (e) {
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
getClients = function (url) {
    url = typeof url !== 'undefined' ? url : timestrapConfig.API_URLS.CLIENTS;
    quickFetch(url).then(function (data) {
        this.update({
            clients: data.results,
            next: data.next,
            previous: data.previous
        });
    }.bind(this));
}.bind(this);

submitClient = function (e) {
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
}.bind(this);

getPerms = function () {
    quickFetch('/api/permissions/').then(function (data) {
        let perms = Object;
        $.each(data.results, function (i, perm) {
            perms[perm.codename] = perm;
        });
        this.perms = perms;
    });
}.bind(this);

this.on('mount', function () {
    getPerms();
    getClients();
}.bind(this));
});

riot.tag2('entries', '<div class="row py-2 mb-4 bg-faded rounded"> <div class="col-12"> <a href="/reports/" class="btn btn-primary btn-sm"> <i class="fa fa-book" aria-hidden="true"></i> Create Reports </a> <pager update="{getEntries}"></pager> </div> </div> <div class="row py-1 bg-inverse text-white font-weight-bold rounded-top"> <div class="col-sm-3 mb-2"> Date </div> <div class="col-sm-3 mb-2"> Task </div> <div class="col-sm-6"> </div> <div class="col-sm-3"> Project </div> <div class="col-sm-5"> Note </div> <div class="col-sm-2"> Duration </div> <div class="col-sm-2"> </div> </div> <form name="entry-add" class="row mb-4 py-2 bg-faded rounded-bottom" onsubmit="{submitEntry}" if="{perms && perms.add_entry}"> <div class="col-sm-3 mb-2"> <input name="entry-date" type="text" class="form-control form-control-sm date-input" ref="date" placeholder="Date"> </div> <div class="col-sm-3"> <select name="entry-task" class="task-select" ref="task"> <option></option> <option each="{tasks}" riot-value="{url}"> {name} </option> </select> </div> <div class="col-sm-6"> </div> <div class="col-sm-3"> <select name="entry-project" class="project-select" ref="project" required> <option></option> <optgroup each="{c in clients}" label="{c}"> <option each="{projects}" riot-value="{url}" if="{c === client_details.name}"> {name} </option> </optgroup> </select> </div> <div class="col-sm-5"> <input name="entry-note" type="text" class="form-control form-control-sm" ref="note" placeholder="Note"> </div> <div class="col-sm-2"> <input name="entry-duration" type="text" class="form-control form-control-sm text-right font-weight-bold" oninput="{timer}" ref="duration" placeholder="0:00" riot-value="{timerDuration}" required> </div> <div class="col-sm-2"> <button name="entry-add-submit" type="submit" class="btn btn-success btn-sm w-100" onclick="{timer}"> {timerState} </button> </div> </form> <div class="mb-4" each="{d in dates}"> <div class="row inset-row"> <div class="col-12"> <h2 class="display-4 text-muted">{moment(d).format(\'LL\')}</h5> </div> </div> <div class="entry-rows rounded"> <entry each="{entries}" if="{d === date}" class="row py-2 bg-faded small" perms="{perms}"></entry> </div> </div> <div class="row bg-success text-white py-2 mb-4 rounded"> <div class="offset-sm-6 col-sm-2 text-right"> Subtotal<br> <strong>Total</strong> </div> <div class="col-sm-2 text-right"> {durationToString(subtotalDuration)}<br> <strong>{durationToString(totalDuration)}</strong> </div> </div>', '', '', function(opts) {
tickTimer = function (entry) {
    ++entry.totalSeconds;
    let hours = pad(Math.floor(entry.totalSeconds / 3600));
    let minutes = pad(Math.floor(entry.totalSeconds % 3600 / 60));
    let seconds = pad(entry.totalSeconds % 3600 % 60);
    entry.update({
        timerDuration: hours + ':' + minutes + ':' + seconds
    });
}.bind(this);

timer = function (e) {
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

getEntries = function (url) {
    let userEntries = timestrapConfig.API_URLS.ENTRIES + '?user=' + timestrapConfig.USER.ID;
    url = typeof url !== 'undefined' ? url : userEntries;

    let entries = quickFetch(url);
    let projects = quickFetch(timestrapConfig.API_URLS.PROJECTS);
    let tasks = quickFetch(timestrapConfig.API_URLS.TASKS);

    Promise.all([entries, projects, tasks]).then(function (e) {
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
            onStart: function () {
                this.set('select', new Date());
            }
        });
    }.bind(this));
}.bind(this);

submitEntry = function (e) {
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
}.bind(this);

updateTotals = function (newDuration, oldDuration) {
    this.totalDuration += newDuration - oldDuration;
    this.subtotalDuration += newDuration - oldDuration;
    this.update();
}.bind(this);

getPerms = function () {
    quickFetch('/api/permissions/').then(function (data) {
        let perms = Object;
        $.each(data.results, function (i, perm) {
            perms[perm.codename] = perm;
        });
        this.perms = perms;
    });
}.bind(this);

this.on('mount', function () {
    this.timerState = 'Start';
    getPerms();
    getEntries();
}.bind(this));
});

riot.tag2('entry', '<virtual if="{!edit}"> <div class="col-sm-3 client-project"> <div class="text-muted small"> {project_details.client_details.name} </div> {project_details.name} </div> <div class="col-sm-5 d-flex flex-column align-self-end tasks"> <div class="text-muted small" if="{task}"> {task_details.name} </div> {note} </div> <virtual if="{!runTimer}"> <div class="col-sm-2 d-flex align-self-center justify-content-end display-4 duration"> {durationToString(duration)} </div> <div class="col-sm-2 d-flex align-self-center justify-content-end"> <virtual if="{perms.change_entry || perms.delete_entry}"> <button name="entry-menu" class="btn btn-faded btn-sm btn-icon dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> <i class="fa fa-ellipsis-v" aria-hidden="true"></i> </button> <div class="dropdown-menu dropdown-menu-right" aria-labelledby="entry-menu"> <a class="dropdown-item entry-menu-restart" href="#" onclick="{entryTimer}" if="{perms.change_entry}"> Restart </a> <a class="dropdown-item entry-menu-change" href="#" onclick="{editEntry}" if="{perms.change_entry}"> Edit </a> <a class="dropdown-item entry-menu-delete" href="#" onclick="{deleteEntry}" if="{perms.delete_entry}"> Delete </a> </div> </virtual> </div> </virtual> <virtual if="{runTimer}"> <div class="col-sm-2"> <input name="entry-duration" type="text" class="form-control form-control-sm text-right font-weight-bold" ref="duration" placeholder="0:00" riot-value="{timerDuration}"> </div> <div class="col-sm-2"> <button name="entry-save" type="submit" class="btn btn-success btn-sm w-100" onclick="{entryTimer}"> {timerState} </div> </button> </virtual> </virtual> <virtual if="{edit}"> <div class="col-sm-3"> <select name="entry-project" class="custom-select custom-select-edit" ref="project" required> <optgroup each="{c in parent.clients}" label="{c}"> <option each="{p in parent.parent.projects}" riot-value="{p.url}" if="{c === p.client_details.name}" selected="{p.id === parent.project_details.id}"> {p.name} </option> </optgroup> </select> </div> <div class="col-sm-5"> <input name="entry-note" type="text" class="form-control form-control-sm" ref="note" placeholder="Note" riot-value="{note}"> </div> <div class="col-sm-2"> <input name="entry-duration" type="text" class="form-control form-control-sm text-right font-weight-bold" ref="duration" placeholder="0:00" riot-value="{durationToString(duration)}"> </div> <div class="col-sm-2"> <button name="entry-save" class="btn btn-success btn-sm w-100" onclick="{saveEntry}"> Save </button> </div> </virtual>', '', '', function(opts) {
editEntry = function (e) {
    e.preventDefault();
    this.edit = true;
    this.update();
    $('.custom-select-edit').select2({
        width: '100%',
        dropdownAutoWidth: true
    });
};

entryTimer = function (e) {
    if (!this.timerState) {
        this.runTimer = true;
        this.timerState = 'Stop';
        let hours = Math.floor(this.duration);
        let minutes = (this.duration - hours) * 60;
        this.totalSeconds = hours * 3600 + minutes * 60;
        tickTimer(this);
        this.interval = setInterval(tickTimer, 1000, this);
        e.preventDefault();
    } else {
        this.timerState = undefined;
        clearInterval(this.interval);
        let dur = this.timerDuration;
        this.runTimer = false;
        this.edit = true;
        this.update();
        this.refs.duration.value = dur.substr(0, dur.lastIndexOf(':'));
        e.preventDefault();
    }
};

saveEntry = function (e) {
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
            updateTotals(this.duration, oldDuration);
        } else {
            this.update();
        }
        toggleButtonBusy(clickedButton);
    }.bind(this));
};

deleteEntry = function (e) {
    e.preventDefault();
    quickFetch(this.url, 'delete').then(function (response) {
        if (response.status === 204) {
            let index = this.parent.entries.indexOf(e.item);
            this.parent.entries.splice(index, 1);
            // updateTotals executes parent update.
            updateTotals(0, this.duration);
        }
    }.bind(this));
};
});

riot.tag2('navigation', '<div class="navbar sticky-top navbar-toggleable-sm navbar-inverse bg-primary mb-4"> <div class="container"> <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarNav"> <span class="navbar-toggler-icon"></span> </button> <a class="navbar-brand" href="{timestrapConfig.CORE_URLS.ENTRIES}"> Timestrap </a> <div id="nav" class="collapse navbar-collapse"> <ul id="nav-app" class="navbar-nav mr-auto"> <virtual if="{timestrapConfig.USER}"> <virtual if="{perms && perms.view_entry}"> <li class="nav-item"> <a id="nav-app-entries" class="nav-link" href="{timestrapConfig.CORE_URLS.ENTRIES}"> Timesheet </a> </li> </virtual> <virtual if="{perms && perms.view_client}"> <li class="nav-item"> <a id="nav-app-clients" class="nav-link" href="{timestrapConfig.CORE_URLS.CLIENTS}"> Clients </a> </li> </virtual> <virtual if="{perms && perms.view_task}"> <li class="nav-item"> <a id="nav-app-tasks" class="nav-link" href="{timestrapConfig.CORE_URLS.TASKS}"> Tasks </a> </li> </virtual> <li class="nav-item"> <a id="nav-app-reports" class="nav-link" href="{timestrapConfig.CORE_URLS.REPORTS}"> Reports </a> </li> </virtual> </ul> <ul id="nav-admin" class="navbar-nav"> <virtual if="{timestrapConfig.USER}"> <li class="nav-item dropdown"> <a class="nav-link dropdown-toggle" data-toggle="dropdown"> {timestrapConfig.USER.NAME} </a> <div class="dropdown-menu dropdown-menu-right"> <a id="nav-admin-api" class="dropdown-item" href="{timestrapConfig.CORE_URLS.API}"> API Browser </a> <a id="nav-admin-admin" class="dropdown-item" href="{timestrapConfig.CORE_URLS.ADMIN}"> Admin </a> <a id="nav-admin-logout" class="dropdown-item" href="{timestrapConfig.CORE_URLS.LOGOUT}"> Logout </a> </div> </li> <li class="nav-item"> <img riot-src="{user.gravatar_url}" width="32" height="32" class="rounded my-1 ml-2"> </li> </virtual> <virtual if="{!timestrapConfig.USER}"> <li class="nav-item"> <a id="nav-admin-login" class="nav-link" href="{timestrapConfig.CORE_URLS.LOGIN}"> Login </a> </li> </virtual> </ul> </div> </div> </div>', '', '', function(opts) {
getPerms = function () {
    quickFetch(timestrapConfig.API_URLS.PERMISSIONS).then(function (data) {
        let perms = Object;
        $.each(data.results, function (i, perm) {
            perms[perm.codename] = perm;
        });
        this.update({
            perms: perms
        });
    }.bind(this));
}.bind(this);

getUser = function () {
    quickFetch(timestrapConfig.USER.URL).then(function (data) {
        this.update({
            user: data
        });
    }.bind(this));
}.bind(this);

this.on('mount', function () {
    if (timestrapConfig.USER) {
        getPerms();
        getUser();
    }
}.bind(this));
});

riot.tag2('pager', '<button class="btn btn-primary btn-sm pull-right" data-url="{this.parent.next}" if="{this.parent.next}" onclick="{loadDataUrl}"> Next <i class="fa fa-arrow-right" aria-hidden="true"></i> </button> <button class="btn btn-primary btn-sm pull-right mr-1" data-url="{this.parent.previous}" if="{this.parent.previous}" onclick="{loadDataUrl}"> <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous </button>', '', '', function(opts) {
loadDataUrl = function (e) {
    this.opts.update(e.currentTarget.getAttribute('data-url'));
};
});

riot.tag2('project', '<virtual if="{edit}"> <div class="col-8"> <input name="project-name" type="text" class="form-control form-control-sm" ref="name" riot-value="{name}"> </div> <div class="col-2"> <input name="project-estimate" type="text" class="form-control form-control-sm" placeholder="Estimate" ref="estimate" riot-value="{estimate}"> </div> <div class="col-2"> <button name="project-save" class="btn btn-success btn-sm w-100" onclick="{saveProject}"> Save </button> </div> </virtual> <virtual if="{!edit}"> <div class="mb-1 col-6">{name}</div> <virtual if="{percent_done}"> <div class="col-4 d-flex align-items-center"> <div class="progress w-100"> <virtual if="{percent_done > 100}"> <div class="progress-bar bg-danger" riot-style="width: {percent_done}%"> {percent_done}% </div> </virtual> <virtual if="{percent_done <= 100}"> <div class="progress-bar" riot-style="width: {percent_done}%"> {percent_done}% </div> </virtual> </div> </div> </virtual> <virtual if="{!percent_done}"> <div class="col-2 d-flex align-items-center"> <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i> <span class="mb-1">{total_duration}</span> </div> <div class="col-2 d-flex align-items-center"> <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i> <span class="mb-1">{total_entries}</span> </div> </virtual> <div class="col-2"> <button name="project-change" class="btn btn-warning btn-sm w-100" onclick="{editProject}" disabled="{!perms.change_project}"> Edit </button> </div> </virtual>', '', '', function(opts) {
editProject = function (e) {
    this.edit = true;
    this.update();
};

saveProject = function (e) {
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

riot.tag2('reports', '<div class="row py-2 mb-4 bg-faded rounded"> <div class="col-12"> <button id="export-report" class="btn btn-primary btn-sm" onclick="{exportReport}"> <i class="fa fa-download" aria-hidden="true"></i> Export Report </button> <select class="custom-select form-control-sm" ref="export_format"> <option value="csv">csv</option> <option value="xls">xls</option> <option value="xlsx">xlsx</option> <option value="tsv">tsv</option> <option value="ods">ods</option> <option value="json">json</option> <option value="yaml">yaml</option> <option value="html">html</option> </select> <pager update="{getEntries}"></pager> </div> </div> <form name="report-filters" class="row mb-4 pt-3 pb-1 bg-faded rounded" onsubmit="{getReport}"> <div class="col-sm-6"> <div class="form-group"> <select id="report-filter-user" ref="user"> <option></option> <option each="{users}" riot-value="{id}">{username}</option> </select> </div> <div class="form-group"> <select id="report-filter-project" ref="project"> <option></option> <optgroup each="{c in clients}" label="{c.name}"> <option each="{p in c.projects}" riot-value="{p.id}"> {p.name} </option> </optgroup> </select> </div> <div class="form-group"> <select id="report-filter-client" ref="client"> <option></option> <option each="{clients}" riot-value="{id}">{name}</option> </select> </div> </div> <div class="col-sm-6"> <div class="form-group"> <select id="report-filter-task" ref="task"> <option></option> <option each="{tasks}" riot-value="{id}">{name}</option> </select> </div> <div class="form-group"> <div class="row"> <div class="col-md-6"> <input id="report-filter-min-date" type="text" class="form-control form-control-sm date-input" ref="min_date" placeholder="Min Date"> </div> <div class="col-md-6"> <input id="report-filter-max-date" type="text" class="form-control form-control-sm date-input" ref="max_date" placeholder="Max Date"> </div> </div> </div> <button id="generate-report" type="submit" class="btn btn-primary btn-sm w-100"> Generate Report </button> </div> </form> <div class="entry-date-group mb-4" each="{dates}"> <div class="row inset-row"> <div class="col-12"> <h2 class="display-4 text-muted">{mainDate}</h5> </div> </div> <div class="entry-rows rounded"> <div class="entry-row row py-2 bg-faded small" each="{entries}" if="{mainDate === date}"> <div class="col-sm-3 client-project"> <div class="text-muted small"> {project_details.client_details.name} </div> {project_details.name} </div> <div class="col-sm-5 d-flex flex-column align-self-end note"> <div class="text-muted small" if="{task}"> {task_details.name} </div> {note} </div> <div class="col-sm-2 d-flex align-self-center justify-content-end display-4 duration"> {durationToString(duration)} </div> <div class="col-sm-2 d-flex align-self-end username"> {user_details.username} </div> </div> </div> </div> <div class="row bg-success text-white py-2 mb-4 rounded"> <div class="offset-sm-6 col-sm-2 text-right"> Subtotal<br> <strong>Total</strong> </div> <div class="col-sm-2 text-right"> {durationToString(subtotalDuration)}<br> <strong>{durationToString(totalDuration)}</strong> </div> </div>', '', '', function(opts) {
getEntries = function (url) {
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
}.bind(this);

getReport = function (e) {
    e.preventDefault();
    query = {
        user: this.refs.user.value,
        project: this.refs.project.value,
        task: this.refs.task.value,
        project__client: this.refs.client.value,
        min_date: this.refs.min_date.value,
        max_date: this.refs.max_date.value
    };
    url = timestrapConfig.API_URLS.ENTRIES + '?' + $.param(query);
    getEntries(url);
}.bind(this);

exportReport = function (e) {
    toggleButtonBusy($('#generate-report'));
    toggleButtonBusy($('#export-report'));
    query = {
        user: this.refs.user.value,
        project: this.refs.project.value,
        project__client: this.refs.client.value,
        min_date: this.refs.min_date.value,
        max_date: this.refs.max_date.value,
        task: this.refs.task.value,
        export_format: this.refs.export_format.value
    };

    // TODO: Use a promise? This doesn't work for button toggling.
    document.location.href = timestrapConfig.CORE_URLS.REPORTS_EXPORT + '?' + $.param(query);
    toggleButtonBusy($('#generate-report'));
    toggleButtonBusy($('#export-report'));
}.bind(this);

this.on('mount', function () {
    getEntries();

    let users = quickFetch(timestrapConfig.API_URLS.USERS);
    let clients = quickFetch(timestrapConfig.API_URLS.CLIENTS);
    let tasks = quickFetch(timestrapConfig.API_URLS.TASKS);

    Promise.all([users, clients, tasks]).then(function (data) {
        this.update({
            users: data[0].results,
            clients: data[1].results,
            tasks: data[2].results
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
        $('#report-filter-task').select2({
            placeholder: 'Tasks',
            width: '100%',
            allowClear: true
        });
    }.bind(this));

    $('.date-input').pickadate({
        format: 'yyyy-mm-dd'
    });
}.bind(this));
});

riot.tag2('task', '<div class="row py-2 bg-faded rounded mb-2"> <virtual if="{edit && perms.change_task}"> <div class="col-8"> <input name="task-name" type="text" class="form-control form-control-sm" ref="name" riot-value="{name}"> </div> <div class="col-2"> <input name="task-rate" type="text" class="form-control form-control-sm" ref="hourly_rate" riot-value="{hourly_rate}"> </div> <div class="col-2"> <button name="task-save" class="btn btn-success btn-sm w-100" onclick="{saveTask}"> Save </button> </div> </virtual> <virtual if="{!edit}"> <div class="col-8 d-flex align-items-center"> <span class="font-weight-bold">{name}</span> </div> <div class="col-2 d-flex align-items-center"> <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i> <span class="mb-1">${hourly_rate}</span> </div> <div class="col-2"> <button name="task-change" class="btn btn-warning btn-sm w-100" onclick="{editTask}" disabled="{!perms.change_task}"> Edit </button> </div> </virtual> </div>', '', '', function(opts) {
editTask = function (e) {
    this.edit = true;
    this.update();
};

saveTask = function (e) {
    e.preventDefault();
    clickedButton = e.target;
    toggleButtonBusy(clickedButton);
    let body = {
        name: this.refs.name.value,
        hourly_rate: this.refs.hourly_rate.value
    };
    quickFetch(this.url, 'put', body).then(function (data) {
        if (data.id) {
            this.name = body.name;
            this.hourly_rate = body.hourly_rate;
        }
        this.name.value = '';
        this.hourly_rate.value = '';
        this.edit = false;
        this.update();
        toggleButtonBusy(clickedButton);
    }.bind(this));
};

this.on('mount', function () {
    this.update();
}.bind(this));
});

riot.tag2('tasks', '<div class="mb-4 clearfix"> <pager update="{getTasks}"></pager> </div> <div class="row py-1 bg-inverse text-white font-weight-bold rounded-top"> <div class="col-sm-8"> Task </div> <div class="col-sm-2"> Hourly Rate </div> <div class="col-sm-2"> </div> </div> <form name="task-add" class="row mb-4 py-2 bg-faded rounded-bottom" onsubmit="{submitTask}" if="{perms && perms.add_task}"> <div class="col-8"> <input name="task-name" type="text" class="form-control form-control-sm" ref="name" placeholder="New Task Name" required> </div> <div class="col-2"> <input name="task-hourly-rate" type="text" class="form-control form-control-sm" ref="hourly_rate" placeholder="Hourly Rate" required> </div> <div class="col-2"> <button name="client-add-submit" type="submit" class="btn btn-success btn-sm w-100"> Add </button> </div> </form> <task each="{tasks}" perms="{perms}"></task>', '', '', function(opts) {
getTasks = function (url) {
    url = typeof url !== 'undefined' ? url : timestrapConfig.API_URLS.TASKS;
    quickFetch(url).then(function (data) {
        this.update({
            tasks: data.results,
            next: data.next,
            previous: data.previous
        });
    }.bind(this));
}.bind(this);

submitTask = function (e) {
    e.preventDefault();
    toggleButtonBusy(e.target);
    let body = {
        name: this.refs.name.value,
        hourly_rate: this.refs.hourly_rate.value
    };
    quickFetch(timestrapConfig.API_URLS.TASKS, 'post', body).then(function (data) {
        this.refs.name.value = '';
        this.refs.hourly_rate.value = '';
        if (data.id) {
            this.tasks.unshift(data);
            this.update();
        }
        toggleButtonBusy(e.target);
    }.bind(this));
}.bind(this);

getPerms = function () {
    quickFetch('/api/permissions/').then(function (data) {
        let perms = Object;
        $.each(data.results, function (i, perm) {
            perms[perm.codename] = perm;
        });
        this.perms = perms;
    });
}.bind(this);

this.on('mount', function () {
    getPerms();
    getTasks();
}.bind(this));
});
