// Mobile Navigation Toggle
const navToggle = document.querySelector(".nav-toggle")
const navMenu = document.querySelector(".nav-menu")

navToggle.addEventListener("click", () => {
  navMenu.classList.toggle("active")

  // Animate hamburger menu
  const bars = navToggle.querySelectorAll(".bar")
  bars.forEach((bar, index) => {
    if (navMenu.classList.contains("active")) {
      if (index === 0) bar.style.transform = "rotate(45deg) translate(5px, 5px)"
      if (index === 1) bar.style.opacity = "0"
      if (index === 2) bar.style.transform = "rotate(-45deg) translate(7px, -6px)"
    } else {
      bar.style.transform = "none"
      bar.style.opacity = "1"
    }
  })
})

// Close mobile menu when clicking on a link
document.querySelectorAll(".nav-link").forEach((link) => {
  link.addEventListener("click", () => {
    navMenu.classList.remove("active")
    const bars = navToggle.querySelectorAll(".bar")
    bars.forEach((bar) => {
      bar.style.transform = "none"
      bar.style.opacity = "1"
    })
  })
})

// Navbar scroll effect
window.addEventListener("scroll", () => {
  const navbar = document.querySelector(".navbar")
  if (window.scrollY > 100) {
    navbar.classList.add("scrolled")
  } else {
    navbar.classList.remove("scrolled")
  }
})

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault()
    const target = document.querySelector(this.getAttribute("href"))
    if (target) {
      const offsetTop = target.offsetTop - 80 // Account for fixed navbar
      window.scrollTo({
        top: offsetTop,
        behavior: "smooth",
      })
    }
  })
})

// Form submission handling
const contactForm = document.querySelector(".contact-form")
if (contactForm) {
  contactForm.addEventListener("submit", function (e) {
    e.preventDefault()

    // Get form data
    const formData = new FormData(this)
    const formObject = {}
    formData.forEach((value, key) => {
      formObject[key] = value
    })

    // Show success message (you can replace this with actual form submission)
    showNotification("Pesan Anda berhasil dikirim! Kami akan segera menghubungi Anda.", "success")

    // Reset form
    this.reset()
  })
}

// Search form handling
const searchForm = document.querySelector(".search-form")
if (searchForm) {
  searchForm.addEventListener("submit", (e) => {
    e.preventDefault()
    showNotification("Pencarian sedang diproses...", "info")
    // Here you would typically handle the search functionality
  })
}

// Property card interactions
document.querySelectorAll(".property-card").forEach((card) => {
  card.addEventListener("click", function () {
    // Get property details from the card
    const propertyTitle = this.querySelector(".property-title").textContent
    const propertyLocation = this.querySelector(".property-location").textContent.trim()
    const propertyPrice = this.querySelector(".property-price").textContent
    const propertyArea = this.getAttribute("data-area")
    const propertyBedrooms = this.getAttribute("data-bedrooms")
    const propertyBathrooms = this.getAttribute("data-bathrooms")

    // Set property details in the modal
    document.getElementById("modal-property-title").textContent = propertyTitle
    // Ambil teks lokasi tanpa menghapus kata pertama
    const fullLocation = propertyLocation.replace(/^\s*/, "").replace(/^\S+\s+/, "") // Hanya hapus icon di awal
    document.getElementById("modal-property-location").textContent = fullLocation

    // Add loading effect to map
    const mapContainer = document.querySelector(".modal-map")
    const mapImage = document.getElementById("modal-map-image")

    mapContainer.classList.add("loading")

    // Set map image based on location with real coordinates
    const locationForMap = fullLocation // Use the full location name

    // Map real locations to coordinates for better accuracy
    let mapCenter = ""
    const zoomLevel = 15

    if (locationForMap.includes("Bintaro")) {
      mapCenter = "-6.2684,106.7316" // Bintaro Sektor 9 coordinates
    } else if (locationForMap.includes("Pondok Indah")) {
      mapCenter = "-6.2659,106.7844" // Pondok Indah coordinates
    } else if (locationForMap.includes("Sudirman")) {
      mapCenter = "-6.2088,106.8229" // Sudirman CBD coordinates
    } else {
      mapCenter = encodeURIComponent(locationForMap)
    }

    // Create a realistic Google Maps static image URL
    const mapImageUrl = `https://maps.googleapis.com/maps/api/staticmap?center=${mapCenter}&zoom=${zoomLevel}&size=500x200&maptype=roadmap&style=feature:all|element:geometry|color:0xf5f5f5&style=feature:all|element:labels.text.fill|color:0x616161&style=feature:all|element:labels.text.stroke|color:0xf5f5f5&style=feature:road|element:geometry|color:0xffffff&style=feature:road|element:labels.text.fill|color:0x9ca5b3&style=feature:water|element:geometry|color:0xc9c9c9&style=feature:poi|element:geometry|color:0xeeeeee&markers=color:0xf19d3b|size:mid|${mapCenter}&key=YOUR_API_KEY`

    // Update map location text with full location name - pastikan menggunakan teks asli dari HTML
    const originalLocationText = this.querySelector(".property-location")
      .textContent.trim()
      .replace(/^\s*/, "")
      .replace(/^\S+\s+/, "")
    document.querySelector(".modal-map-location-text").textContent = originalLocationText

    // Simulate loading delay for better UX
    setTimeout(() => {
      mapImage.setAttribute("src", mapImageUrl)
      mapContainer.classList.remove("loading")
    }, 800)

    // Set Google Maps link with proper coordinates
    let googleMapsUrl = ""
    if (mapCenter.includes(",")) {
      googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${mapCenter}`
    } else {
      googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(locationForMap)}`
    }
    document.getElementById("modal-map-link").setAttribute("href", googleMapsUrl)

    // Show the modal
    openModal()
  })
})

// Modal functionality
function openModal() {
  const modalOverlay = document.getElementById("property-modal-overlay")
  modalOverlay.classList.add("active")
  document.body.style.overflow = "hidden" // Prevent scrolling when modal is open
}

function closeModal() {
  const modalOverlay = document.getElementById("property-modal-overlay")
  modalOverlay.classList.remove("active")
  document.body.style.overflow = "" // Re-enable scrolling
}

// Close modal when clicking outside or on close button
document.addEventListener("DOMContentLoaded", () => {
  const modalOverlay = document.getElementById("property-modal-overlay")
  const closeButton = document.getElementById("modal-close")

  if (modalOverlay) {
    modalOverlay.addEventListener("click", (e) => {
      if (e.target === modalOverlay) {
        closeModal()
      }
    })
  }

  if (closeButton) {
    closeButton.addEventListener("click", closeModal)
  }

  // Handle form submission in modal
  const modalForm = document.getElementById("property-interest-form")
  if (modalForm) {
    modalForm.addEventListener("submit", function (e) {
      e.preventDefault()

      // Get form data
      const name = document.getElementById("modal-name").value
      const phone = document.getElementById("modal-phone").value
      const property = document.getElementById("modal-property-title").textContent

      // Here you would typically send this data to your server
      console.log("Interest form submitted:", { name, phone, property })

      // Show success message
      showNotification(
        `Terima kasih ${name}! Kami akan menghubungi Anda segera untuk properti "${property}"`,
        "success",
      )

      // Close modal
      closeModal()

      // Reset form
      this.reset()
    })
  }
})

// Notification system
function showNotification(message, type = "info") {
  // Remove existing notifications
  const existingNotifications = document.querySelectorAll(".notification")
  existingNotifications.forEach((notification) => notification.remove())

  // Create notification element
  const notification = document.createElement("div")
  notification.className = `notification notification-${type}`
  notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `

  // Add styles
  notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === "success" ? "#27ae60" : type === "error" ? "#e74c3c" : "#3498db"};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
    `

  // Add animation styles
  const style = document.createElement("style")
  style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        .notification-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }
        .notification-close {
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0;
            line-height: 1;
        }
        .notification-close:hover {
            opacity: 0.7;
        }
    `
  document.head.appendChild(style)

  // Add to page
  document.body.appendChild(notification)

  // Close button functionality
  const closeButton = notification.querySelector(".notification-close")
  closeButton.addEventListener("click", () => {
    notification.remove()
  })

  // Auto remove after 5 seconds
  setTimeout(() => {
    if (notification.parentNode) {
      notification.remove()
    }
  }, 5000)
}

// Intersection Observer for animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.animation = "fadeInUp 0.6s ease forwards"
    }
  })
}, observerOptions)

// Observe elements for animation
document.addEventListener("DOMContentLoaded", () => {
  const animateElements = document.querySelectorAll(".property-card, .service-card, .contact-item")
  animateElements.forEach((el) => {
    el.style.opacity = "0"
    el.style.transform = "translateY(30px)"
    observer.observe(el)
  })
})

// Property filter functionality (if needed)
function filterProperties(type) {
  const properties = document.querySelectorAll(".property-card")
  properties.forEach((property) => {
    if (type === "all" || property.dataset.type === type) {
      property.style.display = "block"
    } else {
      property.style.display = "none"
    }
  })
}

// Back to top button
const backToTopButton = document.createElement("button")
backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>'
backToTopButton.className = "back-to-top"
backToTopButton.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #f39c12, #e67e22);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    font-size: 1.2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    z-index: 1000;
`

document.body.appendChild(backToTopButton)

// Show/hide back to top button
window.addEventListener("scroll", () => {
  if (window.scrollY > 300) {
    backToTopButton.style.opacity = "1"
    backToTopButton.style.visibility = "visible"
  } else {
    backToTopButton.style.opacity = "0"
    backToTopButton.style.visibility = "hidden"
  }
})

// Back to top functionality
backToTopButton.addEventListener("click", () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  })
})

// Loading animation for images
document.addEventListener("DOMContentLoaded", () => {
  const images = document.querySelectorAll("img")
  images.forEach((img) => {
    img.addEventListener("load", () => {
      img.style.opacity = "1"
    })

    // Set initial opacity
    img.style.opacity = "0"
    img.style.transition = "opacity 0.3s ease"
  })
})

// Lazy loading for images (simple implementation)
const lazyImages = document.querySelectorAll("img[data-src]")
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const img = entry.target
      img.src = img.dataset.src
      img.removeAttribute("data-src")
      imageObserver.unobserve(img)
    }
  })
})

lazyImages.forEach((img) => imageObserver.observe(img))

// Form validation
function validateForm(form) {
  const inputs = form.querySelectorAll("input[required], textarea[required], select[required]")
  let isValid = true

  inputs.forEach((input) => {
    if (!input.value.trim()) {
      input.style.borderColor = "#e74c3c"
      isValid = false
    } else {
      input.style.borderColor = "#27ae60"
    }
  })

  return isValid
}

// Add form validation to contact form
if (contactForm) {
  const inputs = contactForm.querySelectorAll("input, textarea, select")
  inputs.forEach((input) => {
    input.addEventListener("blur", () => {
      if (input.hasAttribute("required") && !input.value.trim()) {
        input.style.borderColor = "#e74c3c"
      } else {
        input.style.borderColor = "#27ae60"
      }
    })

    input.addEventListener("input", () => {
      if (input.style.borderColor === "rgb(231, 76, 60)" && input.value.trim()) {
        input.style.borderColor = "#27ae60"
      }
    })
  })
}

console.log("Uni Property website loaded successfully!")
