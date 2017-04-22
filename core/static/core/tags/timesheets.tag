<timesheets>
    <table class="timesheets-table table table-striped table-sm w-100 d-none">
        <thead class="thead-inverse">
            <tr>
                <th>Name</th>
            </tr>
        </thead>
        <tbody>
            <tr each={ timesheets }>
                <td>{ name }</td>
            </tr>
        </tbody>
    </table>

    <p class="loading">Loading...</p>

    <script>
        var tag = this;

        fetch('/api/timesheets/?format=json', {
            credentials: 'include'
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            tag.timesheets = data;

            let loading = document.querySelector('.loading');
            loading.classList.toggle('d-none');

            let timesheetsTable = document.querySelector('.timesheets-table');
            timesheetsTable.classList.toggle('d-none');

            tag.update();
        });
    </script>
</timesheets>
