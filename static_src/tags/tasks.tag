<tasks>
    <div class="mb-4 clearfix">
        <pager update={ getTasks }/>
    </div>

    <div class="row py-1 bg-inverse text-white font-weight-bold rounded-top">
        <div class="col-sm-8">
            Task
        </div>
        <div class="col-sm-2">
            Hourly Rate
        </div>
        <div class="col-sm-2">
        </div>
    </div>

    <form name="task-add"
          class="row mb-4 py-2 bg-faded rounded-bottom"
          onsubmit={ submitTask }
          if={ perms && perms.add_task }>
        <div class="col-8">
            <input name="task-name"
                   type="text"
                   class="form-control form-control-sm"
                   ref="name"
                   placeholder="New Task Name"
                   required>
        </div>
        <div class="col-2">
            <input name="task-hourly-rate"
                   type="text"
                   class="form-control form-control-sm"
                   ref="hourly_rate"
                   placeholder="Hourly Rate"
                   required>
        </div>
        <div class="col-2">
            <button
                    name="client-add-submit"
                    type="submit"
                    class="btn btn-success btn-sm w-100">
                Add
            </button>
        </div>
    </form>

    <task each={ tasks } perms={ perms } />


    <script type="es6">
        getTasks = function(url) {
            url = (typeof url !== 'undefined') ? url : timestrapConfig.API_URLS.TASKS;
            quickFetch(url).then(function(data) {
                this.update({
                    tasks: data.results,
                    next: data.next,
                    previous: data.previous
                });
            }.bind(this));
        }.bind(this);


        submitTask = function(e) {
            e.preventDefault();
            toggleButtonBusy(e.target);
            let body = {
                name: this.refs.name.value,
                hourly_rate: this.refs.hourly_rate.value
            };
            quickFetch(timestrapConfig.API_URLS.TASKS, 'post', body).then(function(data) {
                this.refs.name.value = '';
                this.refs.hourly_rate.value = '';
                if (data.id) {
                    this.tasks.unshift(data);
                    this.update();
                }
                toggleButtonBusy(e.target);
            }.bind(this));
        }.bind(this);


        getPerms = function() {
            prefetch.PERMISSIONS.then(function(data) {
                let perms = Object;
                $.each(data.results, function(i, perm) {
                    perms[perm.codename] = perm;
                });
                this.perms = perms;
            });
        }.bind(this);


        this.on('mount', function() {
            getPerms();
            getTasks();
        }.bind(this));
    </script>
</tasks>
