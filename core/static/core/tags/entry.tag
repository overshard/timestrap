<entry>
    <virtual if={ !edit }>
        <div class="col-sm-3">
            <div class="text-muted small">
                { project_details.client_details.name }
            </div>
            { project_details.name }
        </div>
        <div class="col-sm-5 d-flex align-this-end">
            { note }
        </div>
        <virtual if={ !runTimer }>
            <div class="col-sm-2 d-flex align-this-end">
                { duration }
            </div>
            <div class="col-sm-2 d-flex align-this-center justify-content-end">
                <button class="btn btn-faded dropdown-toggle rounded-0"
                        type="button"
                        id="entry-edit-menu"
                        data-toggle="dropdown"
                        aria-haspopup="true"
                        aria-expanded="false">
                    <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
                </button>
                <div class="dropdown-menu dropdown-menu-right"
                     aria-labelledby="entry-edit-menu">
                    <a class="dropdown-item" href="#" onclick={ restartEntry }>
                        Restart
                    </a>
                    <a class="dropdown-item" href="#" onclick={ editEntry }>
                        Edit
                    </a>
                    <a class="dropdown-item" href="#" onclick={ deleteEntry }>
                        Delete
                    </a>
                </div>
            </div>
        </virtual>
        <virtual if={ runTimer }>
            <div class="col-sm-2 d-flex align-this-end">
                <input type="text"
                       class="form-control form-control"
                       ref="duration"
                       placeholder="0:00"
                       value="{ timerDuration }"/>
            </div>
            <div class="col-sm-2 d-flex align-this-center justify-content-end">
                <button type="submit"
                        class="btn btn-success"
                        onclick={ timer }>
                    { timerState }
                </button>
            </div>
        </virtual>
    </virtual>
    <virtual if={ edit }>
        <div class="col-sm-3">
            <select class="custom-select" ref="project">
                <option each={ p in parent.projects }
                        value={ p.url }
                        selected={ p.id == project_details.id }>
                    { p.name }
                </option>
            </select>
        </div>
        <div class="col-sm-5 d-flex align-this-end">
            <input type="text"
                   class="form-control form-control"
                   ref="note"
                   placeholder="Note"
                   value={ note }/>
        </div>
        <div class="col-sm-2 d-flex align-this-end">
            <input type="text"
                   class="form-control form-control"
                   ref="duration"
                   placeholder="0:00"
                   value={ duration }/>
        </div>
        <div class="col-sm-2 d-flex align-this-center justify-content-end">
            <button class="btn btn-success" onclick={ saveEntry }>
                <i class="fa fa-floppy-o" aria-hidden="true"></i> Save
            </button>
        </div>
    </virtual>


    <script>
        editEntry(e) {
            e.preventDefault()
            this.edit = true
            this.update()
        }


        restartEntry(e) {
            e.preventDefault()
            this.runTimer = true
            this.timer(e)
            this.update()
        }


        timer(e) {
            if (!this.timerState) {
                let duration_parts = this.duration.split(':')
                this.timerState = 'Start'
                this.hours = duration_parts[0]
                this.minutes = duration_parts[1]
                this.seconds = 0
                this.timerDuration = pad(this.hours) + ':' + pad(this.minutes) + ':' + pad(this.seconds)
                this.timerState = 'Stop'
                interval = setInterval(this.parent.tick, 1000, this)
                e.preventDefault()
            } else {
                clearInterval(interval);
                this.duration = pad(this.hours) + ':' + pad(this.minutes)
                this.timerState = undefined
                this.runTimer = false
                this.edit = true
                this.update()
                e.preventDefault()
            }
        }


        saveEntry(e) {
            e.preventDefault()
            this.note = this.refs.note.value
            this.duration = this.refs.duration.value
            this.project = this.refs.project.value
            this.project_details = this.parent.projects[this.refs.project.selectedIndex]
            quickFetch(this.url, 'put', this).then(function(data) {
                this.note.value = ''
                this.duration.value = ''
                this.project.value = ''
                this.edit = false
                this.update()
            }.bind(this))
        }


        deleteEntry(e) {
            e.preventDefault()
            quickFetch(this.url, 'delete').then(function() {
                this.unmount()
            }.bind(this))
        }
    </script>
</entry>
