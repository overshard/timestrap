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

    <table class="tasks-table table table-striped table-sm w-100 d-none">
        <thead class="thead-inverse">
            <tr>
                <th>Name</th>
                <th>Timesheet</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            <tr each={ tasks }>
                <td>{ name }</td>
                <td>{ timesheet.name }</td>
                <td class="text-right"><button class="btn btn-primary btn-sm" data-id="{ id }" onclick={ goToEntries }>Entries</button></td>
            </tr>
        </tbody>
    </table>

    <p class="loading text-center my-5">
        <i class="fa fa-spinner" aria-hidden="true"></i>
    </p>

    <script>
        var tag = this;
        var url = '/api/tasks/';

        var loading = null;
        var entriesTable = null;

        function getTasks(url) {
            let location = window.location.href;
            location = location.split('?');
            if (location.length === 2 && !url.includes(location[1])) {
                if (url.split('?').length === 2) {
                    url = url + '&' + location[1];
                } else {
                    url = url + '?' + location[1];
                }
            }

            fetch(url, {
                credentials: 'include',
                headers: new Headers({
                    'content-type': 'application/json',
                })
            }).then(function(response) {
                return response.json();
            }).then(function(data) {
                loading = document.querySelector('.loading');
                tasksTable = document.querySelector('.tasks-table');

                loading.classList.add('d-none');
                tasksTable.classList.remove('d-none');

                tag.update({
                    tasks: data.results,
                    next: data.next,
                    previous: data.previous
                });
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
    </script>
</tasks>
