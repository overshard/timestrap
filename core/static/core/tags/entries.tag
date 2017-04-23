<entries>
    <p class="mb-4 clearfix">
        <button class="btn btn-primary btn-sm"
            data-url="{ previous }"
            if={ previous }
            onclick={ entriesPage }>
            <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous
        </button>

        <button class="btn btn-primary btn-sm pull-right"
            data-url="{ next }"
            if={ next }
            onclick={ entriesPage }>
            Next <i class="fa fa-arrow-right" aria-hidden="true"></i>
        </button>
    </p>

    <form onsubmit={ submitEntry }>
        <table class="entries-table table table-striped table-sm w-100 d-none">
            <thead class="thead-inverse">
                <tr>
                    <th>Date</th>
                    <th>User</th>
                    <th>Duration</th>
                    <th>Note</th>
                    <th>Task</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr class="table-info">
                    <td>
                        <input type="text" class="date-input form-control form-control-sm" ref="date" placeholder="Date">
                    </td>
                    <td>
						<select class="user-select" ref="user">
							<option each={ users } value={ url }>{ username }</option>
						</select>
                    </td>
                    <td>
                        <input type="text" class="form-control form-control-sm" ref="duration" placeholder="Duration">
                    </td>
                    <td>
                        <input type="text" class="form-control form-control-sm" ref="note" placeholder="Note">
                    </td>
                    <td>
						<select class="task-select" ref="task">
							<option each={ tasks } value={ url }>{ name }</option>
						</select>
                    </td>
                    <td class="text-right">
                        <button type="submit" class="btn btn-primary btn-sm">Add</button>
                    </td>
                </tr>
                <tr each={ entries }>
                    <td>{ date }</td>
                    <td>{ user_details.username }</td>
                    <td>{ duration }</td>
                    <td>{ note }</td>
                    <td>{ task_details.name }</td>
                    <td></td>
                </tr>
            </tbody>
        </table>
    </form>

    <p class="loading text-center my-5">
        <i class="fa fa-spinner" aria-hidden="true"></i>
    </p>

    <script>
        var tag = this;
        var loading;
        var entriesTable;

        function getEntries(url) {
            let entries = fetch(url || entriesApiUrl, {
                credentials: 'include',
                headers: new Headers({
                    'content-type': 'application/json',
                })
            }).then(function(response) {
                return response.json();
            })

            let users = fetch(usersApiUrl, {
                credentials: 'include',
                headers: new Headers({
                    'content-type': 'application/json',
                })
            }).then(function(response) {
                return response.json();
            })

            let tasks = fetch(tasksApiUrl, {
                credentials: 'include',
                headers: new Headers({
                    'content-type': 'application/json',
                })
            }).then(function(response) {
                return response.json();
            })

            Promise.all([entries, users, tasks]).then(function(e) {
                loading = document.querySelector('.loading');
                entriesTable = document.querySelector('.entries-table');

                loading.classList.add('d-none');
                entriesTable.classList.remove('d-none');

                tag.update({
                    entries: e[0].results,
                    users: promote(userId, e[1].results),
                    tasks: e[2].results,
                    next: e[0].next,
                    previous: e[0].previous
                });

                $('.date-input').pickadate({
                    format: 'yyyy-mm-dd'
                });
				$('.user-select').chosen();
				$('.task-select').chosen();
            });
        }

        getEntries();

        entriesPage(e) {
            loading.classList.remove('d-none');
            entriesTable.classList.add('d-none');
            getEntries(e.target.dataset.url);
        }

        submitEntry(e) {
            e.preventDefault();
            let csrfToken = Cookies.get('csrftoken');
            let formValues = {
                date: this.refs.date.value,
                user: this.refs.user.value,
                duration: this.refs.duration.value,
                note: this.refs.note.value,
                task: this.refs.task.value
            }
            fetch(entriesApiUrl, {
                credentials: 'include',
                headers: new Headers({
                    'content-type': 'application/json',
                    'X-CSRFToken': csrfToken
                }),
                method: 'post',
                body: JSON.stringify(formValues)
            }).then(function(response) {
                getEntries();
            });
        }
    </script>
</entries>
