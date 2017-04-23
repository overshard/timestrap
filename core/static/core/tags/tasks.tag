<tasks>
    <p class="mb-4 clearfix">
        <button class="btn btn-primary btn-sm"
            data-url="{ previous }"
            if={ previous }
            onclick={ tasksPage }>
            <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous
        </button>

        <button class="btn btn-primary btn-sm pull-right"
            data-url="{ next }"
            if={ next }
            onclick={ tasksPage }>
            Next <i class="fa fa-arrow-right" aria-hidden="true"></i>
        </button>
    </p>

    <form onsubmit={ submitTask }>
        <table class="tasks-table table table-striped table-sm w-100 d-none">
            <thead class="thead-inverse">
                <tr>
                    <th>Name</th>
                    <th>Timesheet</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <input type="text" class="form-control form-control-sm" ref="name" placeholder="Name">
                    </td>
                    <td>
						<select class="timesheet-select" ref="timesheet">
                            <option selected>Timesheet</option>
							<option each={ timesheets } value={ url }>{ name }</option>
						</select>
                    </td>
                    <td class="text-right">
                        <button type="submit" class="btn btn-primary btn-sm">Add</button>
                    </td>
                </tr>
                <tr each={ tasks }>
                    <td>{ name }</td>
                    <td>{ timesheet_details.name }</td>
                    <td class="text-right"><button class="btn btn-primary btn-sm" data-id="{ id }" onclick={ goToEntries }>Entries</button></td>
                </tr>
            </tbody>
        </table>
    </form>

    <p class="loading text-center my-5">
        <i class="fa fa-spinner" aria-hidden="true"></i>
    </p>

    <script>
        var tag = this;
        var url = '/api/tasks/';

        var loading = null;
        var entriesTable = null;

        function getTasks(url) {
            url = appendQuery(url);

            let tasks = fetch(url, {
                credentials: 'include',
                headers: new Headers({
                    'content-type': 'application/json',
                })
            }).then(function(response) {
                return response.json();
            });

            let timesheets = fetch('/api/timesheets/', {
                credentials: 'include',
                headers: new Headers({
                    'content-type': 'application/json',
                })
            }).then(function(response) {
                return response.json();
            });

			Promise.all([tasks, timesheets]).then(function(e) {
                loading = document.querySelector('.loading');
                tasksTable = document.querySelector('.tasks-table');

                loading.classList.add('d-none');
                tasksTable.classList.remove('d-none');

                tag.update({
                    tasks: e[0].results,
                    timesheets: e[1].results,
                    next: e[0].next,
                    previous: e[0].previous
                });

				$('.timesheet-select').chosen();
			});
        }

        getTasks(url);

        tasksPage(e) {
            url = e.target.dataset.url;
            loading.classList.remove('d-none');
            tasksTable.classList.add('d-none');
            getTasks(url);
        }

        goToEntries(e) {
            task = e.target.dataset.id;
            document.location.href = '/entries/?task=' + task;
        }

        submitTask(e) {
            e.preventDefault();
            let csrfToken = Cookies.get('csrftoken');
            let formValues = {
                name: this.refs.name.value,
                timesheet: this.refs.timesheet.value
            }
            fetch(url, {
                credentials: 'include',
                headers: new Headers({
                    'content-type': 'application/json',
                    'X-CSRFToken': csrfToken
                }),
                method: 'post',
                body: JSON.stringify(formValues)
            }).then(function(response) {
                getTasks(url);
            });
        }
    </script>
</tasks>
