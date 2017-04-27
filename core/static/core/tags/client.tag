<client>
    <div class="col-10" if={ !edit }>
        <a class="text-primary" onclick={ goToProjects }>
            <strong>{ name } <i class="fa fa-chevron-down" aria-hidden="true"></i></strong>
        </a>
    </div>
    <div class="col-10" if={ edit }>
        <input type="text" class="form-control form-control-sm" ref="name" value="{ name }" onkeypress="return event.keyCode != 13;">
    </div>
    <div class="col-2 text-right">
        <button if={ !edit } class="btn btn-warning btn-sm" onclick={ editClient }>
            <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Edit
        </button>
        <button if={ edit } class="btn btn-success btn-sm" onclick={ saveClient }>
            <i class="fa fa-floppy-o" aria-hidden="true"></i> Save
        </button>
    </div>


    <script>
        var self = this;
        var edit = false;


        editClient(e) {
            self.edit = true;
            self.update();
        }


        goToProjects(e) {
            document.location.href = projectsUrl + e.item.id;
        }


        saveClient(e) {
            e.preventDefault();
            self.name = self.refs.name.value;
            quickFetch(self.url, 'put', self).then(function(data) {
                self.name.value = '';
                self.edit = false;
                self.update();
            });
        }
    </script>
</client>
