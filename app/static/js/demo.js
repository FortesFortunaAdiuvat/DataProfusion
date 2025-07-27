/*!
 * Demo script for Data Profusion particle background
 */

$(document).ready(function() {
    // Initialize particle ground effect
    $('#particles').particleground({
        minSpeedX: 0.1,
        maxSpeedX: 0.7,
        minSpeedY: 0.1,
        maxSpeedY: 0.7,
        directionX: 'center',
        directionY: 'center',
        density: 10000,
        dotColor: 'rgba(34, 139, 34, 0.6)',
        lineColor: 'rgba(34, 139, 34, 0.2)',
        particleRadius: 4,
        lineWidth: 1,
        curvedLines: false,
        proximity: 100,
        parallax: true,
        parallaxMultiplier: 5
    });

    // Add smooth hover effects for chart links
    $('.chart-link').on('mouseenter', function() {
        $(this).find('.chart-icon').addClass('pulse');
    }).on('mouseleave', function() {
        $(this).find('.chart-icon').removeClass('pulse');
    });

    // Add pulse animation class
    $('<style>')
        .prop('type', 'text/css')
        .html(`
            .pulse {
                animation: pulse 0.6s ease-in-out;
            }
            
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
        `)
        .appendTo('head');

    // Add loading state for external links
    $('.chart-link[target="_blank"]').on('click', function() {
        var $this = $(this);
        var originalContent = $this.find('.chart-title').text();
        
        $this.find('.chart-title').html('<span class="loading"></span> Loading...');
        
        // Reset after 3 seconds (in case the new tab doesn't load)
        setTimeout(function() {
            $this.find('.chart-title').text(originalContent);
        }, 3000);
    });

    // Keyboard navigation support
    $('.chart-link').on('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            $(this)[0].click();
        }
    });

    // Add ARIA labels for accessibility
    $('.chart-link').each(function() {
        var title = $(this).find('.chart-title').text();
        $(this).attr('aria-label', 'Navigate to ' + title + ' dashboard');
    });
});