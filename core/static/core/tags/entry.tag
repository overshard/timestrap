<entry>
    <div class="col-sm-3" if={ !edit }>
        <div class="text-muted small">
            { project_details.client_details.name }
        </div>
        { project_details.name }
    </div>
    <div class="col-sm-3" if={ edit }>
        <select class="custom-select" ref="project">
            <option value='' class="text-muted">Project</option>
            <option each={ parent.projects } value={ url } selected={ id == project_details.id }>{ name }</option>
        </select>
    </div>
    <div class="col-sm-5 d-flex align-self-end" if={ !edit }>
        { note }
    </div>
    <div class="col-sm-5 d-flex align-self-end" if={ edit }>
        <input type="text" class="form-control form-control" ref="note" placeholder="Note" value="{ note }">
    </div>
    <div class="col-sm-2 d-flex align-self-end" if={ !edit && !run_timer }>
        { duration }
    </div>
    <div class="col-sm-2 d-flex align-self-end" if={ edit }>
        <input type="text" class="form-control form-control" ref="duration" placeholder="0:00" value="{ duration }">
    </div>
    <div class="col-sm-2 d-flex align-self-end" if={ run_timer }>
        <input type="text" class="form-control form-control" ref="duration" placeholder="0:00" value="{ timerDuration }">
    </div>
    <div class="col-sm-2 d-flex align-self-center justify-content-end" if={ !edit && !run_timer }>
        <button class="btn btn-secondary dropdown-toggle" type="button" id="entry-edit-menu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
        </button>
        <div class="dropdown-menu" aria-labelledby="entry-edit-menu">
            <a class="dropdown-item" href="#" onclick={ restartEntry }>Restart</a>
            <a class="dropdown-item" href="#" onclick={ editEntry }>Edit</a>
            <a class="dropdown-item" href="#" onclick={ deleteEntry }>Delete</a>
        </div>
    </div>
    <div class="col-sm-2 d-flex align-self-center justify-content-end" if={ edit }>
        <button class="btn btn-success" onclick={ saveEntry }>
            <i class="fa fa-floppy-o" aria-hidden="true"></i> Save
        </button>
    </div>
    <div class="col-sm-2 d-flex align-self-center justify-content-end" if={ run_timer }>
        <button type="submit" class="btn btn-success" onclick={ timer }>{ timerState }</button>
    </div>


    <script>
        var self = this;


        editEntry(e) {
            self.edit = true;
            self.update();
        }


        restartEntry(e) {
            e.preventDefault();
            self.run_timer = true;
            self.timer(e);
            self.update();
        }


        timer(e) {
            if (!self.timerState) {
                let duration_parts = self.duration.split(':');
                self.timerState = 'Start';
                self.hours = duration_parts[0];
                self.minutes = duration_parts[1];
                self.seconds = 0;
                self.timerDuration = pad(self.hours) + ':' + pad(self.minutes) + ':' + pad(self.seconds);
                self.timerState = 'Stop';
                interval = setInterval(self.parent.tick, 1000, self);
                e.preventDefault();
            } else {
                clearInterval(interval);
                self.duration = pad(self.hours) + ':' + pad(self.minutes);
                self.timerState = undefined;
                self.run_timer = false;
                self.edit = true;
                self.update();
                e.preventDefault();
            }
        }


        saveEntry(e) {
            e.preventDefault();
            self.note = self.refs.note.value;
            self.duration = self.refs.duration.value;
            quickFetch(self.url, 'put', self).then(function(data) {
                self.note.value = '';
                self.duration.value = '';
                self.edit = false;
                self.update();
            });
        }


        deleteEntry(e) {
            e.preventDefault();
            quickFetch(self.url, 'delete').then(function() {
                $('#entry-' + self.id).remove();
            });
        }
    </script>
</entry>
