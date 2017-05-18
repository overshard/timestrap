<project>
    <virtual if={ edit }>
        <div class="col-8">
            <input name="project-name"
                   type="text"
                   class="form-control form-control-sm"
                   ref="name"
                   value={ name }/>
        </div>
        <div class="col-2">
            <input name="project-estimate"
                   type="text"
                   class="form-control form-control-sm"
                   placeholder="Estimate"
                   ref="estimate"
                   value={ estimate }/>
        </div>
        <div class="col-2">
            <button name="project-save" class="btn btn-success btn-sm w-100"
                    onclick={ saveProject }>
                Save
            </button>
        </div>
    </virtual>
    <virtual if={ !edit }>
        <div class="mb-1 col-6">{ name }</div>
        <virtual if={ percent_done }>
            <div class="col-4 d-flex align-items-center">
                <div class="progress w-100">
                    <virtual if={ percent_done > 100 }>
                        <div class="progress-bar bg-danger" style="width: { percent_done }%">
                            { percent_done }%
                        </div>
                    </virtual>
                    <virtual if={ percent_done <= 100 }>
                        <div class="progress-bar" style="width: { percent_done }%">
                            { percent_done }%
                        </div>
                    </virtual>
                </div>
            </div>
        </virtual>
        <virtual if={ !percent_done }>
            <div class="col-2 d-flex align-items-center">
                <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
                <span class="mb-1">{ total_duration }</span>
            </div>
            <div class="col-2 d-flex align-items-center">
                <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i>
                <span class="mb-1">{ total_entries }</span>
            </div>
        </virtual>
        <div class="col-2">
            <button name="project-change"
                    class="btn btn-warning btn-sm w-100"
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


        saveProject(e) {
            e.preventDefault();
            clickedButton = e.explicitOriginalTarget;
            toggleButtonBusy(clickedButton);
            let body = {
                client: this.client,
                name: this.refs.name.value,
                estimate: this.refs.estimate.value
            };
            quickFetch(this.url, 'put', body).then(function(data) {
                if (data.id) {
                    this.name = data.name;
                    this.estimate = data.estimate;
                    this.percent_done = data.percent_done;
                }
                this.name.value = '';
                this.edit = false;
                this.update();
                toggleButtonBusy(clickedButton);
            }.bind(this));
        }
    </script>
</project>
