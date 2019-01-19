var app = new Vue({
    el: '#app',
    data: {

        data {
            'brand' : null,
            'models': [],
            'fuel': null,
            'volume': null,
            'mileage': 0,
            'year': null,
            'model': null
        },

        prediction: null

    },
//    delimiters: ['[[',']]'],

    methods: {
        getModels() {
			console.log("Getting organization images ...", this.brand);

            if (this.brand == null) {
                return false;
            }

			let data = {
				brand: this.data.brand
			};

			axios
				.post(
					'/models',
					data
				)
				.then(
					function(response) {
						console.log(response);
                        this.models = response.data;

                        this.$forceUpdate();
					}.bind(this)
				)
				.catch(function(error) {
					console.log(error);
				});
		},

		submit() {
		    console.log('Submitting');

            if (this.brand == null) {
                return false;
            }



			axios
				.post(
					'/predict',
					this.data
				)
				.then(
					function(response) {
						console.log(response);
                        this.prediction = response.data;

                        this.$forceUpdate();
					}.bind(this)
				)
				.catch(function(error) {
					console.log(error);
				});
		}
    }
});