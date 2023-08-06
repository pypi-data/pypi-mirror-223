const ActivityCompletedSwitcherApp = {
    data() {
        return {
            ACT_IS_COMPLETED: 'Activity completed',
            ACT_NOT_COMPLETED: 'Mark as completed',
            ACT_UPDATING: 'Updating status...',
            completion_status: this.ACT_UPDATING,
            activity_id: 0,
            activity_completed: false,
            activity_visits: 0,
            SWITCH_URL: '/lxp/activity/completed/'
        }
    },
    beforeMount(){
        // get initial status from server-side template
        this.activity_id = document.getElementById('activity_completed_switch')
            .getAttribute('activity_id') || '0';
        this.activity_completed = this.parseBool(
            document.getElementById('activity_completed_switch')
            .getAttribute('activity_completed') || false);
        this.activity_visits = document.getElementById('activity_completed_switch')
            .getAttribute('activity_visits') || '0';

    },
    mounted() {
            this.initAxios()
            this.updateUserActivityStatus()
    },
    methods: {
        initAxios() {
            // ensure axios calls are seen as ajax - otherwise wagtail returns wrong template
            axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = 'X-CSRFToken'
        },
        reverseStatus() {
            if (this.completion_status === this.ACT_UPDATING) {
                return; // do not allow another call while updating
            }
            this.completion_status = this.ACT_UPDATING
            axios
                .post(this.SWITCH_URL, {'id': this.activity_id, 'action': 'switch'})
                .then(response => {
                    if (response.data.status !== 'ok') {
                        console.log('Ajax error')
                        alert('Application experienced a problem while updating the status. ' +
                            'Please contact the website administrator.')
                        this.updateUserActivityStatus()
                        return
                    }
                    this.activity_completed = response.data.completed
                    this.updateUserActivityStatus()
            })
        },
        updateUserActivityStatus() {
            this.completion_status = (this.activity_completed
                ? this.ACT_IS_COMPLETED
                : this.ACT_NOT_COMPLETED)
        },
        parseBool(val) {
            return val === true || val.toLowerCase() === "true"
        },
    }
}

const acsa = Vue.createApp(ActivityCompletedSwitcherApp)
acsa.mount('#activity_completed_switch')

document.addEventListener("DOMContentLoaded", function(event) {

const showNavbar = (toggleId, navId, bodyId, headerId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId),
    bodypd = document.getElementById(bodyId),
    headerpd = document.getElementById(headerId)

    // Validate that all variables exist
    if(toggle && nav && bodypd && headerpd){
        toggle.addEventListener('click', ()=>
        {
            // show navbar
            nav.classList.toggle('show')
            // // change icon
            // toggle.classList.toggle('toggle-x')
            // add padding to body
            bodypd.classList.toggle('sidenav-pd')
            // add padding to header
            headerpd.classList.toggle('sidenav-pd')
            // swap visibility of all .hide-closed or .hide-open elements
            let elements = document.querySelectorAll('.hide-open');
            for(let i=0; i<elements.length; i++){
                elements[i].classList.toggle('d-none')
            }
            elements = document.querySelectorAll('.hide-open-md');
            for(let i=0; i<elements.length; i++){
                elements[i].classList.toggle('d-md-inline')
            }

        })
    }
}

showNavbar('header-toggle','nav-bar','lxp-content','header')

/*===== LINK ACTIVE =====*/
const linkColor = document.querySelectorAll('.nav_link')

function colorLink(){
if(linkColor){
linkColor.forEach(l=> l.classList.remove('active'))
this.classList.add('active')
}
}
linkColor.forEach(l=> l.addEventListener('click', colorLink))

// Your code to run since DOM is loaded and ready
});