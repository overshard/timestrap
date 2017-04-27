<client>
    <div class="row mb-2 py-2 bg-faded">
        <div class="col-10" if={ !edit }>
            <a class="text-primary" onclick={ showProjects }>
                <strong>{ name } <i class="fa fa-chevron-down" aria-hidden="true"></i></strong>
            </a>
        </div>
        <div class="col-10" if={ edit }>
            <input type="text" class="form-control form-control-sm" ref="name" value="{ name }">
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

    <div class="row mb-1 ml-3 py-1 bg-faded"
         each={ projects }
         data-is="project"
         if={ productsShown }>
    </div>


    <script>
        var self = this;


        editClient(e) {
            self.edit = true;
            self.update();
        }


        showProjects(e) {
            self.productsShown = !self.productsShown;
            self.update();
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


        submitProject(e) {
            e.preventDefault();
            let body = {
                name: self.refs.project_name.value,
                client: self.url
            }
            console.log(body);
            quickFetch(projectsApiUrl, 'post', body).then(function(data) {
                self.refs.project_name.value = '';
                self.projects.unshift(data);
                self.update();
            });
        }
    </script>
</client>
