function validateForm(event) {
    event.preventDefault();
    
    // Get form elements
    const fullName = document.getElementById('fullName').value;
    const jobRole = document.getElementById('jobRole').value;
    const resumeFile = document.getElementById('resume').files[0];
    const fileError = document.getElementById('fileError');
    
    // Clear previous error messages
    fileError.textContent = '';
    
    // Validate full name
    if (fullName.trim().length < 2) {
        alert('Please enter a valid full name');
        return false;
    }
    
    // Validate job role
    if (jobRole.trim().length < 2) {
        alert('Please enter a valid job role');
        return false;
    }
    
    // Validate resume file
    if (resumeFile) {
        // Check file type
        if (!resumeFile.type.includes('pdf')) {
            fileError.textContent = 'Please upload a PDF file only';
            return false;
        }
        
        // Check file size (5MB limit)
        if (resumeFile.size > 5 * 1024 * 1024) {
            fileError.textContent = 'File size should be less than 5MB';
            return false;
        }
    } else {
        fileError.textContent = 'Please upload your resume';
        return false;
    }
    
    // If all validations pass, store the data
    const formData = {
        fullName: fullName,
        jobRole: jobRole,
        resumeFile: resumeFile.name
    };
    
    // Store data in localStorage
    localStorage.setItem('candidateData', JSON.stringify(formData));
    
    // Redirect to interview setup page
    window.location.href = 'interview-setup.html';
    
    return false;
}