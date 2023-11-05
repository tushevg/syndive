
// // Define a function to observe element visibility
// function observeElementVisibility() {
//     // Function to check if the element is out of view
//     function checkElementVisibility(entries, observer) {
//         entries.forEach(entry => {
//             const elementToHide = document.getElementById('id-searchbar-header')
//             if (entry.isIntersecting) {
//                 console.log("Element is in view");
//                 elementToHide.style.display = 'none';
//             } else {
//                 console.log("Element is out of view");
//                 elementToHide.style.display = 'block';
//             }

//             // Apply the style to all children
//             const elementToHideChildren = elementToHide.children;
//             for (let i = 0; i < elementToHideChildren.length; i++) {
//                 elementToHideChildren[i].style.display = elementToHide.style.display;
//             }

//         });
//     }

//     // Create an Intersection Observer instance
//     const observer = new IntersectionObserver(checkElementVisibility);

//     // Select the element to monitor by its ID
//     const elementToMonitor = document.getElementById('id-searchbar-about');
    
//     // Start observing the element
//     observer.observe(elementToMonitor);
// }

// // Use window.onload to ensure the code runs after the page has fully loaded
// window.onload = function () {
//     observeElementVisibility();
// };
