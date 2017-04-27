<project>
    <div class="col-10" if={ !edit }>
        <a class="text-primary" onclick={ goToEntries }>
            { name }
        </a>
    </div>
    <div class="col-10" if={ edit }>
        <input type="text" class="form-control form-control-sm" ref="name" value="{ name }">
    </div>
    <div class="col-2 text-right">
        <button if={ !edit } class="btn btn-warning btn-sm" onclick={ editProject }>
            <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Edit
        </button>
        <button if={ edit } class="btn btn-success btn-sm" onclick={ saveProject }>
            <i class="fa fa-floppy-o" aria-hidden="true"></i> Save
        </button>
    </div>


    <script>
        var self = this;


        editProject(e) {
            self.edit = true;
            self.update();
        }


        goToEntries(e) {
            let query = {
                project: e.item.id
            }
            document.location.href = entriesUrl + '?' + $.param(query);
        }


        saveProject(e) {
            e.preventDefault();
            self.name = self.refs.name.value;
            quickFetch(self.url, 'put', self).then(function(data) {
                self.name.value = '';
                self.edit = false;
                self.update();
            });
        }
    </script>
</project>
