<template>
<div class="container">
    <div class="row py-1 bg-inverse text-white font-weight-bold rounded-top">
        <div class="col-3">
            Created
        </div>
        <div class="col-5">
            Client
        </div>
        <div class="col-2">
            Amount
        </div>
        <div class="col-2">
            Paid?
        </div>
    </div>

    <div class="entry-rows">
        <template v-for="(invoice, index) in invoices"
                  v-bind:invoice="invoice">
            <div v-bind:class="['task', {'bg-danger': invoice.paid === null, 'bg-success': invoice.paid !== null}, 'row', 'py-2', 'text-white']"
                 v-bind:key="invoice.id">
                <div class="col-3">
                    {{ moment(invoice.created) }}
                </div>
                <div class="col-5">
                    {{ invoice.client_details.name }}
                </div>
                <div class="col-2">
                    ${{ invoice.amount }}
                </div>
                <div class="col-2">
                    {{ moment(invoice.paid) }}
                </div>
            </div>
        </template>
    </div>
</div>
</template>


<script>
export default {
    data() {
        return {
            invoices: null
        };
    },
    methods: {
        getInvoices(url) {
            url = (typeof url !== 'undefined') ? url : timestrapConfig.API_URLS.INVOICES;

            let invoicesFetch = this.$quickFetch(url);

            invoicesFetch.then(data => {
                this.invoices = data;
            });
        },
        moment(date) {
            if (date) {
                return moment(date).tz(timestrapConfig.SITE.TIMEZONE).format('LL');
            } else {
                return 'Not Paid';
            }
        }
    },
    mounted() {
        return this.getInvoices();
    },
};
</script>
