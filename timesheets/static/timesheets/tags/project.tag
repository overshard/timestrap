<project>
    <virtual if={ edit }>
        <div class="col-10">
            <input type="text"
                   class="form-control form-control-sm"
                   ref="name"
                   value={ name }/>
        </div>
        <div class="col-2">
            <button class="btn btn-success btn-sm w-100"
                    onclick={ saveProject }>
                Save
            </button>
        </div>
    </virtual>
    <virtual if={ !edit }>
        <a class="text-primary col-6" onclick={ goToEntries }>
            <span class="mb-1">{ name }</span>
            <i class="fa fa-arrow-right ml-2" aria-hidden="true"></i>
        </a>
        <div class="col-2 d-flex align-items-center">
            <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
            <span class="mb-1">{ total_duration }</span>
        </div>
        <div class="col-2 d-flex align-items-center">
            <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i>
            <span class="mb-1">{ total_entries }</span>
        </div>
        <div class="col-2">
            <button class="btn btn-warning btn-sm w-100"
                    onclick={ editProject }
                    disabled={ !perms.change_project }>
                Edit
            </button>
        </div>
    </virtual>


    <script>
        editProject(e) {
            this.edit = true;
            this.update();
        }


        goToEntries(e) {
            let query = {
                project: e.item.id
            };
            document.location.href = entriesUrl + '?' + $.param(query);
        }


        saveProject(e) {
            e.preventDefault();
            let body = {
                client: this.client,
                name: this.refs.name.value
            };
            quickFetch(this.url, 'put', body).then(function(data) {
                if (data.id) {
                    this.name = body.name;
                }
                this.name.value = '';
                this.edit = false;
                this.update();
            }.bind(this));
        }
    </script>
</project>
