<task>
    <div class="row py-2 bg-faded rounded mb-2">
        <virtual if={ edit && perms.change_task }>
            <div class="col-8">
                <input name="task-name"
                       type="text"
                       class="form-control form-control-sm"
                       ref="name"
                       value={ name } />
            </div>
            <div class="col-2">
                <input name="task-rate"
                       type="text"
                       class="form-control form-control-sm"
                       ref="hourly_rate"
                       value={ hourly_rate } />
            </div>
            <div class="col-2">
                <button name="task-save"
                        class="btn btn-success btn-sm w-100"
                        onclick={ saveTask }>
                    Save
                </button>
            </div>
        </virtual>
        <virtual if={ !edit }>
            <div class="col-8 d-flex align-items-center">
                <span class="font-weight-bold">{ name }</span>
            </div>
            <div class="col-2 d-flex align-items-center">
                <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
                <span class="mb-1">${ hourly_rate }</span>
            </div>
            <div class="col-2">
                <button name="task-change"
                        class="btn btn-warning btn-sm w-100"
                        onclick={ editTask }
                        disabled={ !perms.change_task }>
                    Edit
                </button>
            </div>
        </virtual>
    </div>


    <script type="es6">
        this.editTask = function(e) {
            this.edit = true;
            this.update();
        };


        this.saveTask = function(e) {
            e.preventDefault();
            clickedButton = e.target;
            toggleButtonBusy(clickedButton);
            let body = {
                name: this.refs.name.value,
                hourly_rate: this.refs.hourly_rate.value
            };
            quickFetch(this.url, 'put', body).then(function(data) {
                if (data.id) {
                    this.name = body.name;
                    this.hourly_rate = body.hourly_rate;
                }
                this.name.value = '';
                this.hourly_rate.value = '';
                this.edit = false;
                this.update();
                toggleButtonBusy(clickedButton);
            }.bind(this));
        };

        this.on('mount', function() {
            this.update();
        }.bind(this));
    </script>
</task>
