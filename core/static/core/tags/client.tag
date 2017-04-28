<client>
    <div class="row mb-2 py-2 bg-faded">
        <div class="col-10" if={ !edit }>
            <a class="text-primary" onclick={ showProjects }>
                <strong>{ name } <i class="fa fa-chevron-down" aria-hidden="true"></i></strong>
            </a>
        </div>
        <div class="col-10" if={ edit }>
            <input type="text" class="form-control form-control-sm" ref="name" value={ name }>
        </div>
        <div class="col-2 text-right">
            <button if={ !edit } class="btn btn-warning btn-sm" onclick={ editClient }>
                <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Edit
            </button>
            <button if={ edit } class="btn btn-success btn-sm" onclick={ saveClient }>
                <i class="fa fa-floppy-o" aria-hidden="true"></i> Save
            </button>
        </div>
    </div>

    <form onsubmit={ submitProject } if={ productsShown }>
        <div class="row mb-1 ml-3 form-row bg-primary">
            <div class="col-9">
                <input type="text" class="form-control bg-primary" ref="project_name" placeholder="New Project Name">
            </div>
            <div class="col-3 text-right">
                <button type="submit" class="btn btn-primary">
                    <i class="fa fa-plus" aria-hidden="true"></i> Add
                </button>
            </div>
        </div>
    </form>

    <div class="row mb-1 ml-3 py-1 bg-faded" each={ projects } data-is="project" if={ productsShown }/>


    <script>
        editClient(e) {
            this.edit = true
            this.update()
        }


        showProjects(e) {
            this.productsShown = !this.productsShown
            this.update()
        }


        saveClient(e) {
            e.preventDefault()
            this.name = this.refs.name.value
            quickFetch(this.url, 'put', this).then(function(data) {
                this.name.value = ''
                this.edit = false
                this.update()
            }.bind(this));
        }


        submitProject(e) {
            e.preventDefault()
            let body = {
                name: this.refs.project_name.value,
                client: this.url
            }
            quickFetch(projectsApiUrl, 'post', body).then(function(data) {
                this.refs.project_name.value = ''
                this.projects.unshift(data)
                this.update()
            }.bind(this));
        }
    </script>
</client>
