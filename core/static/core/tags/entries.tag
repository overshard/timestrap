<entries>
    <table class="entries-table table table-striped table-sm w-100 d-none">
        <thead class="thead-inverse">
            <tr>
                <th>Date</th>
                <th>User</th>
                <th>Duration</th>
                <th>Note</th>
            </tr>
        </thead>
        <tbody>
            <tr each={ entries }>
                <td>{ date }</td>
                <td>{ user.username }</td>
                <td>{ duration }</td>
                <td>{ note }</td>
            </tr>
        </tbody>
    </table>

    <p class="loading">Loading...</p>

    <script>
        var tag = this;

        fetch('/api/entries/?format=json', {
            credentials: 'include'
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            tag.entries = data;

            let loading = document.querySelector('.loading');
            loading.classList.toggle('d-none');

            let entriesTable = document.querySelector('.entries-table');
            entriesTable.classList.toggle('d-none');

            tag.update();
        });
    </script>
</entries>
