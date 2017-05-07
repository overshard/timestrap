<entry>
    <virtual if={ !edit }>
        <div class="col-sm-3">
            <div class="text-muted small">
                { project_details.client_details.name }
            </div>
            { project_details.name }
        </div>
        <div class="col-sm-5 d-flex align-self-center">
            { note }
        </div>
        <virtual if={ !runTimer }>
            <div class="col-sm-2 d-flex align-self-center justify-content-end font-weight-bold">
                { durationToString(duration) }
            </div>
            <div class="col-sm-2 d-flex align-self-center"
                 if={ perms.change_entry || perms.delete_entry }>
                <button class="btn btn-faded btn-sm w-100 btn-icon dropdown-toggle"
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
            </div>
        </virtual>
        <virtual if={ runTimer }>
            <input type="text"
                   class="form-control form-control col-sm-2"
                   ref="duration"
                   placeholder="0:00"
                   value="{ timerDuration }"/>
            <button type="submit"
                    class="btn btn-success col-sm-2"
                    onclick={ timer }>
                { timerState }
            </button>
        </virtual>
    </virtual>
    <virtual if={ edit }>
        <select class="custom-select col-sm-3"
                ref="project">
            <option each={ p in parent.projects }
                    value={ p.url }
                    selected={ p.id == project_details.id }>
                { p.name }
            </option>
        </select>
        <input type="text"
               class="form-control form-control col-sm-5"
               ref="note"
               placeholder="Note"
               value={ note }/>
        <input type="text"
               class="form-control form-control col-sm-2"
               ref="duration"
               placeholder="0:00"
               value={ durationToString(duration) }/>
        <button class="btn btn-success col-sm-2 rounded-0"
                onclick={ saveEntry }>
            Save
        </button>
    </virtual>


    <script>
        editEntry(e) {
            e.preventDefault();
            this.edit = true;
            this.update();
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
