<tasks>
    <table class="tasks-table table table-striped table-sm w-100 d-none">
        <thead class="thead-inverse">
            <tr>
                <th>Name</th>
            </tr>
        </thead>
        <tbody>
            <tr each={ tasks }>
                <td>{ name }</td>
            </tr>
        </tbody>
    </table>

    <p class="loading">Loading...</p>

    <script>
        var tag = this;

        fetch('/api/tasks/?format=json', {
            credentials: 'include'
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            tag.tasks = data;

            let loading = document.querySelector('.loading');
            loading.classList.toggle('d-none');

            let tasksTable = document.querySelector('.tasks-table');
            tasksTable.classList.toggle('d-none');

            tag.update();
        });
    </script>
</tasks>
