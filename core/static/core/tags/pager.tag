<pager>
    <p class="mb-4 clearfix">
        <button class="btn btn-primary btn-sm"
                data-url="{ this.parent.previous }"
                if={ this.parent.previous }
                onclick={ loadDataUrl }>
            <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous
        </button>

        <button class="btn btn-primary btn-sm pull-right"
                data-url="{ this.parent.next }"
                if={ this.parent.next }
                onclick={ loadDataUrl }>
            Next <i class="fa fa-arrow-right" aria-hidden="true"></i>
        </button>
    </p>


    <script>
        var self = this;


        loadDataUrl(e) {
            self.opts.update(e.currentTarget.getAttribute('data-url'));
        }
    </script>
</pager>
