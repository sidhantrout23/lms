document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const courseList = document.getElementById('courseList');
    const courseTitle = document.getElementById('courseTitle');
    const courseDescription = document.getElementById('courseDescription');
    const materialsList = document.getElementById('materialsList');
    const courseProgress = document.getElementById('courseProgress');
    const addMaterialForm = document.getElementById('addMaterialForm');
    const teacherCoursesList = document.getElementById('teacherCoursesList');
    const addCourseForm = document.getElementById('addCourseForm');
    const usernameDisplay = document.getElementById('usernameDisplay');
    const logoutButton = document.getElementById('logoutButton');
    
    const userId = localStorage.getItem('userId');
    

    if (userId) {
        fetch(`/api/enrollments/${userId}`)
            .then(response => response.json())
            .then(data => {
                usernameDisplay.textContent = localStorage.getItem('username') || 'Guest';
                data.forEach(enrollment => {
                    const li = document.createElement('li');
                    li.innerHTML = `<a href="/course/${enrollment.course_id}"></a>`;
                    courseList.appendChild(li);
                });
            })
            .catch(error => console.error('Error:', error));
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(registerForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                document.getElementById('registerMessage').innerText = result.message;
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(loginForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                if (response.ok) {
                    localStorage.setItem('token', result.token);
                    localStorage.setItem('userId', result.user_id);
                    localStorage.setItem('username', result.username);
                    localStorage.setItem('isTeacher', JSON.stringify(result.is_teacher));
                    window.location.href = '/dashboard';
                } else {
                    document.getElementById('loginMessage').innerText = result.message;
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }

    if (courseList) {
        const userId = localStorage.getItem('userId');
        fetch(`/api/enrollments/${userId}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(enrollment => {
                    const li = document.createElement('li');
                    li.innerText = `Course ID: ${enrollment.course_id}`;
                    const link = document.createElement('a');
                    link.href = `/course/${enrollment.course_id}`;
                    link.textContent = ` View Course `;
                    
                    li.appendChild(link);
                    courseList.appendChild(li);
                });
            })
            .catch(error => console.error('Error:', error));
    }

    if (courseTitle && courseDescription && materialsList && courseProgress) {
        const courseId = document.querySelector('body').dataset.courseId;

        fetch(`/api/courses/${courseId}`)
            .then(response => response.json())
            .then(course => {
                courseTitle.innerText = course.title;
                courseDescription.innerText = course.description;
                course.materials.forEach(material => {
                    const li = document.createElement('li');
                    li.innerHTML = `<a href="${material.url}" target="_blank">${material.filename}</a>`;
                    materialsList.appendChild(li);
                });
                courseProgress.innerText = `Progress: ${course.progress}%`;
            })
            .catch(error => console.error('Error:', error));
    }

    if (addMaterialForm) {
        addMaterialForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(addMaterialForm);

            try {
                const courseId = document.querySelector('body').dataset.courseId;
                const response = await fetch(`/api/courses/${courseId}/materials`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    },
                    body: formData
                });
                const result = await response.json();
                document.getElementById('addMaterialMessage').innerText = result.message;
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }

    if (addCourseForm) {
        addCourseForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(addCourseForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/api/courses', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                document.getElementById('addCourseMessage').innerText = result.message;
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }

    if (teacherCoursesList) {
        const teacherId = localStorage.getItem('userId');

        fetch(`/api/teacher/${teacherId}/courses`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        })
        .then(response => response.json())
        .then(data => {
            data.forEach(course => {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${course.title}</strong><p>${course.description}</p>`;
                teacherCoursesList.appendChild(li);
            });
        })
        .catch(error => console.error('Error:', error));
    }

    if (usernameDisplay) {
        const username = localStorage.getItem('username');
        usernameDisplay.innerText = username || 'Guest';
    }

    function enrollInCourse(courseId) {
        const userId = localStorage.getItem('userId');

        fetch('/api/enroll', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ user_id: userId, course_id: courseId })
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    }

    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            fetch('/logout', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            })
            .then(response => {
                if (response.ok) {
                    localStorage.removeItem('token');
                    localStorage.removeItem('userId');
                    localStorage.removeItem('username');
                    localStorage.removeItem('isTeacher');
                    window.location.href = '/';
                } else {
                    console.error('Logout failed');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    const allCoursesList = document.getElementById('allCoursesList');

    if (allCoursesList) {
        fetch('/api/courses')
            .then(response => response.json())
            .then(courses => {
                courses.forEach(course => {
                    const li = document.createElement('li');
                    li.innerHTML = `<strong>${course.title}</strong><p>${course.description}</p>`;
                    
                    // Add "Enroll" button if not a teacher
                    if (!isTeacher) {
                        const enrollButton = document.createElement('button');
                        enrollButton.innerText = 'Enroll';
                        enrollButton.addEventListener('click', () => enrollInCourse(course.id));
                        li.appendChild(enrollButton);
                    }

                    // Add click event to redirect to course details
                    li.addEventListener('click', () => {
                        window.location.href = `/course/${course.id}`;
                    });

                    allCoursesList.appendChild(li);
                });
            })
            .catch(error => console.error('Error:', error));
    }

    function enrollInCourse(courseId) {
        const userId = localStorage.getItem('userId');

        fetch('/api/enroll', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ user_id: userId, course_id: courseId })
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    }
});
