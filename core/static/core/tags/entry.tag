<entry>
    <virtual if={ !edit }>
        <div class="col-sm-3">
            <div class="text-muted small">
                { project_details.client_details.name }
            </div>
            { project_details.name }
        </div>
        <div class="col-sm-5 d-flex align-self-end">
            { note }
        </div>
        <virtual if={ !runTimer }>
            <div class="col-sm-2 d-flex align-self-end">
                { duration }
            </div>
            <div class="col-sm-2 d-flex align-self-center justify-content-end">
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
            <div class="col-sm-2 d-flex align-self-end">
                <input type="text"
                       class="form-control form-control"
                       ref="duration"
                       placeholder="0:00"
                       value="{ timerDuration }"/>
            </div>
            <div class="col-sm-2 d-flex align-self-center justify-content-end">
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
        <div class="col-sm-5 d-flex align-self-end">
            <input type="text"
                   class="form-control form-control"
                   ref="note"
                   placeholder="Note"
                   value={ note }/>
        </div>
        <div class="col-sm-2 d-flex align-self-end">
            <input type="text"
                   class="form-control form-control"
                   ref="duration"
                   placeholder="0:00"
                   value={ duration }/>
        </div>
        <div class="col-sm-2 d-flex align-self-center justify-content-end">
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
            this.runTimer = true
            this.timer(e)
        }


        timer(e) {
            if (!this.timerState) {
                this.timerState = 'Stop'
                let durSplit = this.duration.split(':')
                this.totalSeconds = (durSplit[0] * 3600) + (durSplit[1] * 60)
                this.parent.tick(this)
                interval = setInterval(this.parent.tick, 1000, this)
                e.preventDefault()
            } else {
                this.timerState = undefined
                clearInterval(interval);
                let dur = this.timerDuration
                this.timerDuration = dur.substr(0, dur.lastIndexOf(':'))
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
