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

    <p class="loading text-center my-5">
        <i class="fa fa-spinner" aria-hidden="true"></i>
    </p>

    <script>
        var tag = this;
        var url = '/api/entries/?format=json';

        var loading = null;
        var entriesTable = null;

        function getEntries(url) {
            fetch(url, {
                credentials: 'include'
            }).then(function(response) {
                return response.json();
            }).then(function(data) {
                loading = document.querySelector('.loading');
                entriesTable = document.querySelector('.entries-table');

                loading.classList.add('d-none');
                entriesTable.classList.remove('d-none');

                tag.update({
                    entries: data.results,
                    next: data.next,
                    previous: data.previous
                });
            });
        }

        getEntries(url);

        entriesPage(e) {
            url = e.target.dataset.url;
            loading.classList.remove('d-none');
            entriesTable.classList.add('d-none');
            getEntries(url);
        }
    </script>
</entries>
