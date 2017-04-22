<entries>
    <table>
        <thead>
            <tr>
                <th>User</th>
                <th>Duration</th>
                <th>Note</th>
            </tr>
        </thead>
        <tbody>
            <tr each={ entries }>
                <td>{ user }</td>
                <td>{ duration }</td>
                <td>{ note }</td>
            </tr>
        </tbody>
    </table>

    <p class="loading">Loading...</p>

    <style>
        .hidden {
            display: none;
        }
    </style>

    <script>
        var tag = this;

        fetch('/api/entries/?format=json', {
            credentials: 'include'
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            tag.entries = data;
            var loading = document.querySelector('.loading');
            loading.classList.toggle('hidden');
            tag.update();
        });
    </script>
</entries>
