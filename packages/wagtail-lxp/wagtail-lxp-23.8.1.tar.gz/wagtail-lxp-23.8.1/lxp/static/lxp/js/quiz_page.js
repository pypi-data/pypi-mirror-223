const QuizPageApp = {
    data() {
        return {
            quiz_id: 0,
            /**
             * Records all answers keyed by item uid
             */
            answers: {},
            /**
             * Tracks all items in the quiz by reference,
             * used e.g. to detect if all qs are answered
             */
            itemRefs: [],
            SUBMIT_URL: '/lxp/quiz/submit/',
            submitted: false,
            score: null,
            score_visible: false

        }
    },
    beforeMount() {
        // get initial status from server-side template
        this.quiz_id = document.getElementById('qapp')
            .getAttribute('quiz_id') || '0';
    },
    beforeUpdate() {
        /**
         * clear refs array as it will be auto-updated
         */
        this.itemRefs = []
    },
    mounted() {
            this.initAxios()
    },
    methods: {
        selectAnswer(key, value) {
            this.answers[key] = value
        },
        /**
         * store refs to all items in quiz
         */
        setItemRef(el) {
            if (el) {
                this.itemRefs.push(el)
            }
        },
        confirmClearAnswers() {
            if (confirm('Are you sure you want to clear all your answers on this page?\n\nNote: this will not erase your earlier attempts.')) {
                this.resetQuiz()
            }

        },
        resetQuiz() {
                this.answers = {}
                this.submitted = false
                this.score = 0
                this.score_visible = 0
        },
        initAxios() {
            // ensure axios calls are seen as ajax - otherwise wagtail returns wrong template
            axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = 'X-CSRFToken'
        },
        confirmSubmitAnswers() {
            if (this.itemRefs.length === Object.keys(this.answers).length) {
                return this.submitAnswers()
            } else {
                if (confirm('You have not answered all questions. Are you sure you want to submit?')) {
                    return this.submitAnswers()
                }
            }
        },
        submitAnswers() {
            console.log("Submitting...")
            if (this.submitted) {
                alert('You cannot submit twice')
                return
            }
            this.submitted = true
            axios
                .post(this.SUBMIT_URL, {'id': this.quiz_id, 'answers': this.answers})
                .then(response => {
                    if (response.data.status !== 'ok') {
                        console.log('Ajax error')
                        alert('There was a technical problem submitting your answers. ' +
                            'Please contact the website administrator.')
                        return
                    }
                    this.showScore(response.data.score)
                    if (response.data.feedback) {
                        this.showFeedback(response.data.feedback)
                    }
            })
        },
        showScore(score) {
            this.score = score
            this.score_visible = true
        },
        showFeedback(feedback) {

        }
    },
}

const qapp = Vue.createApp(QuizPageApp)
qapp.mount('#qapp')