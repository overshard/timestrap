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
        editProject(e) {
            this.edit = true
            this.update()
        }


        goToEntries(e) {
            let query = {
                project: e.item.id
            }
            document.location.href = entriesUrl + '?' + $.param(query)
        }


        saveProject(e) {
            e.preventDefault()
            this.name = this.refs.name.value
            quickFetch(this.url, 'put', this).then(function(data) {
                this.name.value = ''
                this.edit = false
                this.update()
            }.bind(this));
        }
    </script>
</project>
