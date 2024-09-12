document.addEventListener('DOMContentLoaded', (event) => {
    // Function to fetch and display latest jobs
    const fetchLatestJobs = async () => {
        try {
            const response = await fetch('/api/jobs');
            const jobs = await response.json();
            const jobList = document.getElementById('latest-jobs');
            
            if (jobList) {
                jobList.innerHTML = '';
                jobs.forEach(job => {
                    const jobElement = document.createElement('div');
                    jobElement.classList.add('job-listing');
                    jobElement.innerHTML = `
                        <h3>${job.title}</h3>
                        <p>Location: ${job.location}</p>
                        <p>Salary: ${job.salary}</p>
                        <p>Posted: ${new Date(job.created_at).toLocaleDateString()}</p>
                        <a href="/job/${job.id}">View Details</a>
                    `;
                    jobList.appendChild(jobElement);
                });
            }
        } catch (error) {
            console.error('Error fetching latest jobs:', error);
        }
    };

    // Call fetchLatestJobs on page load
    fetchLatestJobs();

    // Set up search functionality
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const searchQuery = document.getElementById('search-input').value;
            window.location.href = `/search?q=${encodeURIComponent(searchQuery)}`;
        });
    }

    // Set up language switcher
    const languageSwitcher = document.getElementById('language-switcher');
    if (languageSwitcher) {
        languageSwitcher.addEventListener('change', (e) => {
            const selectedLanguage = e.target.value;
            document.cookie = `language=${selectedLanguage}; path=/`;
            window.location.reload();
        });
    }
});
