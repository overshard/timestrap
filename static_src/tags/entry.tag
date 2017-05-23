<entry>
    <virtual if={ !edit }>
        <div class="col-sm-3 client-project">
            <div class="text-muted small">
                { project_details.client_details.name }
            </div>
            { project_details.name }
        </div>
        <div class="col-sm-5 d-flex flex-column align-self-end tasks">
            <div class="text-muted small"
                 if={ task }>
                { task_details.name }
            </div>
            { note }
        </div>
        <virtual if={ !runTimer }>
            <div class="col-sm-2 d-flex align-self-center justify-content-end display-4 duration">
                { durationToString(duration) }
            </div>
            <div class="col-sm-2 d-flex align-self-center justify-content-end">
                <virtual if={ perms.change_entry || perms.delete_entry }>
                    <button name="entry-menu"
                            class="btn btn-faded btn-sm btn-icon dropdown-toggle"
                            type="button"
                            data-toggle="dropdown"
                            aria-haspopup="true"
                            aria-expanded="false">
                        <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
                    </button>
                    <div class="dropdown-menu dropdown-menu-right"
                         aria-labelledby="entry-menu">
                        <a class="dropdown-item entry-menu-restart"
                           href="#"
                           onclick={ entryTimer }
                           if={ perms.change_entry }>
                            Restart
                        </a>
                        <a class="dropdown-item entry-menu-change"
                           href="#"
                           onclick={ editEntry }
                           if={ perms.change_entry }>
                            Edit
                        </a>
                        <a class="dropdown-item entry-menu-delete"
                           href="#"
                           onclick={ deleteEntry }
                           if={ perms.delete_entry }>
                            Delete
                        </a>
                    </div>
                </virtual>
            </div>
        </virtual>
        <virtual if={ runTimer }>
            <div class="col-sm-2">
                <input name="entry-duration"
                       type="text"
                       class="form-control form-control-sm text-right font-weight-bold"
                       ref="duration"
                       placeholder="0:00"
                       value="{ timerDuration }"/>
            </div>
            <div class="col-sm-2">
                <button name="entry-save"
                        type="submit"
                        class="btn btn-success btn-sm w-100"
                        onclick={ entryTimer }>
                    { timerState }
            </div>
            </button>
        </virtual>
    </virtual>
    <virtual if={ edit }>
        <div class="col-sm-3">
            <!-- FIXME: Something is buggy about parent.project_details.id -->
            <select id="entry-project"
                    class="custom-select custom-select-edit"
                    ref="project"
                    required>
                <optgroup each={ c in parent.clients } label={ c }>
                    <option each={ p in parent.parent.projects }
                            value={ p.url }
                            if={ c === p.client_details.name }
                            selected={ p.id === parent.project_details.id }>
                        { p.name }
                    </option>
                </optgroup>
            </select>
        </div>
        <div class="col-sm-5">
            <input name="entry-note"
                   type="text"
                   class="form-control form-control-sm"
                   ref="note"
                   placeholder="Note"
                   value={ note }/>
        </div>
        <div class="col-sm-2">
            <input name="entry-duration"
                   type="text"
                   class="form-control form-control-sm text-right font-weight-bold"
                   ref="duration"
                   placeholder="0:00"
                   value={ durationToString(duration) }/>
        </div>
        <div class="col-sm-2">
            <button name="entry-save" class="btn btn-success btn-sm w-100"
                    onclick={ saveEntry }>
                Save
            </button>
        </div>
    </virtual>


    <script type="es6">
        editEntry = function(e) {
            e.preventDefault();
            this.edit = true;
            this.update();
            $('.custom-select-edit').select2({
                width: '100%',
                dropdownAutoWidth: true
            });
        };


        entryTimer = function(e) {
            if (!this.timerState) {
                this.runTimer = true;
                this.timerState = 'Stop';
                let hours = Math.floor(this.duration);
                let minutes = (this.duration - hours) * 60;
                this.totalSeconds = (hours * 3600) + (minutes * 60);
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


        saveEntry = function(e) {
            e.preventDefault();
            clickedButton = e.target;
            toggleButtonBusy(clickedButton);
            let body = {
                user: this.user,
                project: this.refs.project.value,
                note: this.refs.note.value,
                duration: this.refs.duration.value,
            };
            quickFetch(this.url, 'put', body).then(function(data) {
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
                }
                else {
                    this.update();
                }
                toggleButtonBusy(clickedButton);
            }.bind(this));
        };


        deleteEntry = function(e) {
            e.preventDefault();
            quickFetch(this.url, 'delete').then(function(response) {
                if (response.status === 204) {
                    let index = this.parent.entries.indexOf(e.item);
                    this.parent.entries.splice(index, 1);
                    // updateTotals executes parent update.
                    updateTotals(0, this.duration);
                }
            }.bind(this));
        };
    </script>
</entry>
