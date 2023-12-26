function enroll(student_id, course_name){
    // when student is clicking on enroll button
    let url = "enroll/";
    // sending POST request to this url with json data of course_name and student_id
    fetch(url, {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({"course_name":course_name, "user_id":student_id}),
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log(`Data: ${data}`)
            if(data == false){
                alert("You can't register more than 2 trainings, if you failed in one, contact instructor to let you retake or register a training.")
            }
            else if(data == null){
                alert("You already registered this course.")
            }
            else{
                total_user_registered_courses = document.getElementById("courses-total");
                total_user_registered_courses.innerHTML = data
            }

        })
}
