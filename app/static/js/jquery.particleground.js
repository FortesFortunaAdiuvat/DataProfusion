/*!
 * Particle Ground - A simple particle system for web backgrounds
 * Simplified version for Data Profusion
 */

(function($) {
    'use strict';

    function ParticleGround(element, options) {
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');
        var particles = [];
        var raf;

        var settings = $.extend({
            minSpeedX: 0.1,
            maxSpeedX: 0.7,
            minSpeedY: 0.1,
            maxSpeedY: 0.7,
            directionX: 'center',
            directionY: 'center',
            density: 10000,
            dotColor: '#228B22',
            lineColor: '#228B22',
            particleRadius: 7,
            lineWidth: 1,
            curvedLines: false,
            proximity: 100,
            parallax: true,
            parallaxMultiplier: 5,
            onInit: function() {},
            onDestroy: function() {}
        }, options);

        function init() {
            canvas.className = 'pg-canvas';
            canvas.style.display = 'block';
            element.appendChild(canvas);

            resizeCanvas();
            createParticles();
            animate();

            $(window).on('resize', resizeCanvas);
            
            if (settings.parallax) {
                $(window).on('mousemove', updateParallax);
            }

            settings.onInit();
        }

        function resizeCanvas() {
            canvas.width = element.offsetWidth;
            canvas.height = element.offsetHeight;
        }

        function createParticles() {
            var numParticles = Math.round((canvas.width * canvas.height) / settings.density);
            
            for (var i = 0; i < numParticles; i++) {
                particles.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    vx: (Math.random() * (settings.maxSpeedX - settings.minSpeedX) + settings.minSpeedX) * (Math.random() > 0.5 ? 1 : -1),
                    vy: (Math.random() * (settings.maxSpeedY - settings.minSpeedY) + settings.minSpeedY) * (Math.random() > 0.5 ? 1 : -1)
                });
            }
        }

        function updateParallax(e) {
            var centerX = canvas.width / 2;
            var centerY = canvas.height / 2;
            var offsetX = (e.clientX - centerX) / settings.parallaxMultiplier;
            var offsetY = (e.clientY - centerY) / settings.parallaxMultiplier;

            particles.forEach(function(particle) {
                particle.parallaxX = offsetX;
                particle.parallaxY = offsetY;
            });
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            particles.forEach(function(particle) {
                // Update position
                particle.x += particle.vx;
                particle.y += particle.vy;

                // Wrap around edges
                if (particle.x < 0) particle.x = canvas.width;
                if (particle.x > canvas.width) particle.x = 0;
                if (particle.y < 0) particle.y = canvas.height;
                if (particle.y > canvas.height) particle.y = 0;

                // Draw particle
                ctx.beginPath();
                ctx.arc(
                    particle.x + (particle.parallaxX || 0),
                    particle.y + (particle.parallaxY || 0),
                    settings.particleRadius,
                    0,
                    Math.PI * 2
                );
                ctx.fillStyle = settings.dotColor;
                ctx.globalAlpha = 0.6;
                ctx.fill();
            });

            raf = requestAnimationFrame(animate);
        }

        function destroy() {
            if (raf) {
                cancelAnimationFrame(raf);
            }
            $(window).off('resize', resizeCanvas);
            $(window).off('mousemove', updateParallax);
            element.removeChild(canvas);
            settings.onDestroy();
        }

        init();

        return {
            destroy: destroy
        };
    }

    $.fn.particleground = function(options) {
        return this.each(function() {
            var element = this;
            if (!$.data(element, 'plugin_particleground')) {
                $.data(element, 'plugin_particleground', new ParticleGround(element, options));
            }
        });
    };

})(jQuery);