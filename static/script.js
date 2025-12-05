/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNav() {
  document.getElementById("mySidebar").style.width = "750px";
  document.getElementById("main").style.marginLeft = "750px";
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}

/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNavall() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
  document.getElementById("first_main").style.marginLeft = "250px";
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNavall() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
  document.getElementById("first_main").style.marginLeft = "0";
}



document.addEventListener("DOMContentLoaded", function () {
    const containers = document.querySelectorAll(".like-btn-container");

    containers.forEach(container => {
        const btn = container.querySelector(".like-btn");
        const likeCountSpan = container.querySelector(".like-count");
        
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            const cid = this.dataset.cid;

            // Create ripple effect
            const ripple = document.createElement('div');
            ripple.className = 'ripple';
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 800);

            // Create particle explosion
            createParticles(this);

            // Add pulsing glow
            const glow = document.createElement('div');
            glow.className = 'pulse-glow';
            this.appendChild(glow);
            setTimeout(() => glow.remove(), 1500);

            // Add liked animation class
            this.classList.add('liked');

            // Your existing fetch logic
            fetch(`/like/${cid}`, {
                method: "POST"
            })
            .then(res => res.json())
            .then(data => {
                console.log("Like response:", data);
                if (data.worked) {
                    // Animate the count change
                    animateCount(likeCountSpan, data.likes);
                    
                    // Keep liked state if count increased
                    if (data.likes > parseInt(likeCountSpan.textContent)) {
                        // Already has liked class
                    } else {
                        // Unlike - remove liked class
                        setTimeout(() => this.classList.remove('liked'), 600);
                    }
                } else {
                    console.error("Server error:", data.error);
                    // Remove liked class on error
                    setTimeout(() => this.classList.remove('liked'), 600);
                }
            })
            .catch(err => {
                console.error("Like error:", err);
                setTimeout(() => this.classList.remove('liked'), 600);
            });
        });
    });

    // Helper function to create particle explosion
    function createParticles(button) {
        const colors = ['#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#ffd89b', '#19d4ff'];
        const particleCount = 12;

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            const angle = (i * 360) / particleCount;
            
            particle.style.cssText = `
                background: ${colors[i % colors.length]};
                --angle: ${angle}deg;
            `;
            
            button.appendChild(particle);
            setTimeout(() => particle.remove(), 800);
        }
    }

    // Helper function to animate count changes
    function animateCount(element, newCount) {
        const currentCount = parseInt(element.textContent) || 0;
        
        if (newCount !== currentCount) {
            element.style.transition = 'transform 0.3s ease, color 0.3s ease';
            element.style.transform = 'scale(1.3)';
            element.style.color = '#fbbf24';
        }
        
        element.textContent = newCount;
        
        setTimeout(() => {
            element.style.transform = 'scale(1)';
            element.style.color = '';
        }, 300);
    }
});


