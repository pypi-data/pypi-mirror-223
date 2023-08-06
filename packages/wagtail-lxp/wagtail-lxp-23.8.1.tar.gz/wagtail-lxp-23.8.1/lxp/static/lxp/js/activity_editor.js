document.addEventListener("DOMContentLoaded", () => {

    /* Upon selection of an icon in activity page, adds a matching content block to the activity */

    if (document.querySelector("body").classList.contains('model-activitypage')) {

        const icon_input = document.querySelector("select[name=icon]")
        const icon_display_map = {
            "default.svg": "None",
            "pdf.svg": "local_pdf",
            "html.svg": "rich_text",
            "website.svg": "website_url",
            "local_page.svg": "local_page",
            "video_youtube.svg": "embedded_video",
            "video_vimeo.svg": "embedded_video",
        }

        icon_input.addEventListener("change", (event) => {
            let icon_value = event.target.value
            let button_class = 'c-sf-button action-add-block-' + icon_display_map[icon_value]
            let block2display = document.querySelector(`button[class=\'${button_class}\']`)
            if (typeof (block2display) != 'undefined' && block2display != null) {
                block2display.click()
            }
        });

    } // endif body.classList.contains('model-activitypage')
});