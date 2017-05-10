<client>
    <div class="row py-2 bg-faded rounded">
        <virtual if={ edit && perms.change_client }>
            <div class="col-10">
                <input type="text"
                       class="form-control form-control-sm"
                       ref="name"
                       value={ name }/>
            </div>
            <div class="col-2">
                <button class="btn btn-success btn-sm w-100"
                        onclick={ saveClient }>
                    Save
                </button>
            </div>
        </virtual>
        <virtual if={ !edit }>
            <div class="col-6 d-flex align-items-center">
                <a class="text-primary font-weight-bold" onclick={ showProjects } if={ perms.view_project }>
                    <i class="fa fa-chevron-circle-{ chevron } small mr-2" aria-hidden="true"></i>
                    <span class="mb-1">{ name }</span>
                </a>
                <span class="text-primary font-weight-bold" if={ !perms.view_project }>{ name }</span>
            </div>
            <div class="col-2 d-flex align-items-center">
                <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
                <span class="mb-1">{ total_duration }</span>
            </div>
            <div class="col-2 d-flex align-items-center">
                <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i>
                <span class="mb-1">{ total_projects }</span>
            </div>
            <div class="col-2">
                <button class="btn btn-warning btn-sm w-100"
                        onclick={ editClient }
                        disabled={ !perms.change_client }>
                    Edit
                </button>
            </div>
        </virtual>
    </div>

    <form name="project-add" onsubmit={ submitProject } if={ productsShown && perms.add_project }>
        <div class="row bg-faded py-2">
            <div class="col-8">
                <input name="project-name"
                       type="text"
                       class="form-control form-control-sm"
                       ref="project_name"
                       placeholder="New Project Name"
                       required/>
            </div>
            <div class="col-2">
                <input type="text"
                       class="form-control form-control-sm"
                       placeholder="Estimate"
                       ref="estimate"
                       value={ estimate }/>
            </div>
            <div class="col-2">
                <button type="submit"
                        class="btn btn-success btn-sm w-100">
                    Add
                </button>
            </div>
        </div>
    </form>

    <div class="mb-2 project-rows">
        <project class="row py-1 bg-faded"
                 each={ projects }
                 data-is="project"
                 if={ productsShown && perms.view_project }
                 perms={ perms } />
    </div>


    <script>
        editClient(e) {
            this.edit = true;
            this.update();
        }


        showProjects(e) {
            this.productsShown = !this.productsShown;
            if (this.chevron === 'down') {
                this.chevron = 'up';
            } else {
                this.chevron = 'down';
            }
            this.update();
        }


        saveClient(e) {
            e.preventDefault();
            let body = {
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


        submitProject(e) {
            e.preventDefault();
            let body = {
                name: this.refs.project_name.value,
                estimate: this .refs.estimate.value,
                client: this.url
            };
            quickFetch(projectsApiUrl, 'post', body).then(function(data) {
                this.refs.project_name.value = '';
                if (data.id) {
                    this.projects.unshift(data);
                    this.update();
                }
            }.bind(this));
        }

        this.on('mount', function() {
            this.chevron = 'down';
            this.update();
        }.bind(this));
    </script>
</client>
