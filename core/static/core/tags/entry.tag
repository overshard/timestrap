<entry>
    <div class="col-sm-3">
        <div class="text-muted small">
            { project_details.client_details.name }
        </div>
        { project_details.name }
    </div>
    <div class="col-sm-5 d-flex align-self-end" if={ !edit }>
        { note }
    </div>
    <div class="col-sm-5 d-flex align-self-end" if={ edit }>
        <input type="text" class="form-control form-control" ref="note" placeholder="Note" value="{ note }">
    </div>
    <div class="col-sm-2 d-flex align-self-end" if={ !edit }>
        { duration }
    </div>
    <div class="col-sm-2 d-flex align-self-end" if={ edit }>
        <input type="text" class="form-control form-control" ref="duration" placeholder="0:00" value="{ duration }">
    </div>
    <div class="col-sm-2 d-flex align-self-center justify-content-end" if={ !edit }>
        <button class="btn btn-secondary dropdown-toggle" type="button" id="entry-edit-menu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
        </button>
        <div class="dropdown-menu" aria-labelledby="entry-edit-menu">
            <a class="dropdown-item" href="#">Restart</a>
            <a class="dropdown-item" href="#" onclick={ editEntry }>Edit</a>
            <a class="dropdown-item" href="#" onclick={ deleteEntry }>Delete</a>
        </div>
    </div>
    <div class="col-sm-2 d-flex align-self-center justify-content-end" if={ edit }>
        <button class="btn btn-success btn-sm" onclick={ saveEntry }>
            <i class="fa fa-floppy-o" aria-hidden="true"></i> Save
        </button>
    </div>


    <script>
        var self = this;


        editEntry(e) {
            self.edit = true;
            self.update();
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
