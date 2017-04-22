<timesheets>
    <p class="mb-4 clearfix">
        <button class="btn btn-primary btn-sm"
            data-url="{ previous }"
            if={ previous }
            onclick={ timesheetsPage }>
            <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous
        </button>

        <button class="btn btn-primary btn-sm pull-right"
            data-url="{ next }"
            if={ next }
            onclick={ timesheetsPage }>
            Next <i class="fa fa-arrow-right" aria-hidden="true"></i>
        </button>
    </p>

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

    <p class="loading text-center my-5">
        <i class="fa fa-spinner" aria-hidden="true"></i>
    </p>

    <script>
        var tag = this;
        var url = '/api/timesheets/?format=json';

        var loading = null;
        var timesheetsTable = null;

        function getTimesheets(url) {
            fetch(url, {
                credentials: 'include'
            }).then(function(response) {
                return response.json();
            }).then(function(data) {
                loading = document.querySelector('.loading');
                timesheetsTable = document.querySelector('.timesheets-table');

                loading.classList.add('d-none');
                timesheetsTable.classList.remove('d-none');

                tag.update({
                    timesheets: data.results,
                    next: data.next,
                    previous: data.previous
                });
            });
        }

        getTimesheets(url);

        timesheetsPage(e) {
            url = e.target.dataset.url;
            loading.classList.remove('d-none');
            timesheetsTable.classList.add('d-none');
            getTimesheets(url);
        }
    </script>
</timesheets>
