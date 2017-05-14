<entry>
    <virtual if={ !edit }>
        <div class="col-sm-3 client-project">
            <div class="text-muted small">
                { project_details.client_details.name }
            </div>
            { project_details.name }
        </div>
        <div class="col-sm-5 d-flex align-self-end note">
            { note }
        </div>
        <virtual if={ !runTimer }>
            <div class="col-sm-2 d-flex align-self-center justify-content-end display-4 duration">
                { durationToString(duration) }
            </div>
            <div class="col-sm-2 d-flex align-self-center justify-content-end">
                <virtual if={ perms.change_entry || perms.delete_entry }>
                    <button class="btn btn-faded btn-sm btn-icon dropdown-toggle"
                            type="button"
                            id="entry-edit-menu"
                            data-toggle="dropdown"
                            aria-haspopup="true"
                            aria-expanded="false">
                        <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
                    </button>
                    <div class="dropdown-menu dropdown-menu-right"
                         aria-labelledby="entry-edit-menu">
                        <a class="dropdown-item"
                           href="#"
                           onclick={ restartEntry }
                           if={ perms.change_entry }>
                            Restart
                        </a>
                        <a class="dropdown-item"
                           href="#"
                           onclick={ editEntry }
                           if={ perms.change_entry }>
                            Edit
                        </a>
                        <a class="dropdown-item"
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
                <input type="text"
                       class="form-control form-control-sm text-right font-weight-bold"
                       ref="duration"
                       placeholder="0:00"
                       value="{ timerDuration }"/>
            </div>
            <div class="col-sm-2">
                <button type="submit"
                        class="btn btn-success btn-sm w-100"
                        onclick={ timer }>
                    { timerState }
            </div>
            </button>
        </virtual>
    </virtual>
    <virtual if={ edit }>
        <div class="col-sm-3">
            <!-- FIXME: Something is buggy about parent.project_details.id -->
            <select class="custom-select custom-select-edit" ref="project" required>
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
            <input type="text"
                   class="form-control form-control-sm"
                   ref="note"
                   placeholder="Note"
                   value={ note }/>
        </div>
        <div class="col-sm-2">
            <input type="text"
                   class="form-control form-control-sm text-right font-weight-bold"
                   ref="duration"
                   placeholder="0:00"
                   value={ durationToString(duration) }/>
        </div>
        <div class="col-sm-2">
            <button class="btn btn-success btn-sm w-100"
                    onclick={ saveEntry }>
                Save
            </button>
        </div>
    </virtual>


    <script>
        editEntry(e) {
            e.preventDefault();
            this.edit = true;
            this.update();
            $('.custom-select-edit').select2({
                width: '100%',
                dropdownAutoWidth: true
            });
        }


        restartEntry(e) {
            this.runTimer = true;
            this.timer(e);
        }


        timer(e) {
            if (!this.timerState) {
                this.timerState = 'Stop';
                let hours = Math.floor(this.duration);
                let minutes = (this.duration - hours) * 60;
                this.totalSeconds = (hours * 3600) + (minutes * 60);
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
        }


        saveEntry(e) {
            e.preventDefault();
            clickedButton = e.explicitOriginalTarget;
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
                    this.parent.updateTotals(this.duration, oldDuration);
                }
                else {
                    this.update();
                }
                toggleButtonBusy(clickedButton);
            }.bind(this));
        }


        deleteEntry(e) {
            e.preventDefault();
            quickFetch(this.url, 'delete').then(function(response) {
                if (response.status === 204) {
                    let index = this.parent.entries.indexOf(e.item);
                    this.parent.entries.splice(index, 1);
                    // updateTotals executes parent update.
                    this.parent.updateTotals(0, this.duration);
                }
            }.bind(this));
        }
    </script>
</entry>
