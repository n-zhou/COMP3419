import javafx.geometry.Point3D;
import java.util.Random;

ArrayList<PImage> texturePool;
ArrayList<Ball> balls;
Random rand;

void setup() {
    size(700,700,P3D);
    texturePool = new ArrayList<PImage>();
    texturePool.add(loadImage("earth.jpg"));
    texturePool.add(loadImage("obama.jpg"));
    texturePool.add(loadImage("moon.jpg"));
    texturePool.add(loadImage("reddit.jpg"));
    texturePool.add(loadImage("trump.jpg"));
    texturePool.add(loadImage("usa.png"));
    texturePool.add(loadImage("hillary.jpg"));
    texturePool.add(loadImage("scomo.jpg"));
    texturePool.add(loadImage("tones.jpg"));
    texturePool.add(loadImage("farage.jpg"));
    balls = new ArrayList<Ball>();
    rand = new java.util.Random();
}

void draw() {
    background(0);
    pointLight(255, 255, 255, width/2, height/2, 400);
    for (int i = 0; i < balls.size(); ++i) {
        for (int j = i + 1; j < balls.size(); ++j) {
            balls.get(i).resolveCollision(balls.get(j));
        }
        balls.get(i).draw();
    }
    translate(width/2, height/2, -700/2);
    stroke(255);
    noFill();
    box(700,700,700);
}

void mousePressed() {
    balls.add(new Ball(new Point3D(mouseX, mouseY, 0)));
}

class Ball {

    Point3D point;
    Point3D velocity;
    final int RADIUS = 45;
    PShape sphere;
    int lastFrameCount = 0;

    Ball(Point3D point) {
        this.point = point;
        sphere = createShape(SPHERE, RADIUS);
        sphere.setStroke(false);
        sphere.setTexture(texturePool.get(rand.nextInt(texturePool.size())));

        int vX = (rand.nextInt() % 2 == 0) ? rand.nextInt(100): -rand.nextInt(100);
        int vY = (rand.nextInt() % 2 == 0) ? rand.nextInt(100): -rand.nextInt(100);
        int vZ = -rand.nextInt(100);
        velocity = new Point3D(vX,vY,vZ);
    }

    void draw() {
        pushMatrix();
        translate((int)point.getX(), (int)point.getY(), (int)point.getZ());
        if (velocity.magnitude() > 0.1) {
            rotateY(radians(frameCount));
            lastFrameCount = frameCount;
        } else {
            rotateY(radians(lastFrameCount));
        }
        shape(sphere);


        if (point.getX() + RADIUS >= width) {
            if (velocity.getX() >= 0) {
                Point3D delta = new Point3D(2*velocity.getX(), 0,0);
                velocity = velocity.subtract(delta);
            }
        } else if (point.getX() - RADIUS <= 0) {
            if (velocity.getX() <= 0){
                Point3D delta = new Point3D(2*velocity.getX(), 0,0);
                velocity = velocity.subtract(delta);
            }
        }

        if (point.getY() + RADIUS >= height) {
            if (velocity.getY() >= 0) {
                Point3D delta = new Point3D(0, 2*velocity.getY(),0);
                velocity = velocity.subtract(delta);
            }
        } else if (point.getY() - RADIUS <= 0) {
            if (velocity.getY() <= 0){
                Point3D delta = new Point3D(0, 2*velocity.getY(),0);
                velocity = velocity.subtract(delta);
            }
        }

        if (point.getZ() - RADIUS <= -700) {
            if (velocity.getZ() <= 0) {
                Point3D delta = new Point3D(0,0,2*velocity.getZ());
                velocity = velocity.subtract(delta);
            }
        } else if (point.getZ() + RADIUS >= 0) {
            if (velocity.getZ() >= 0) {
                Point3D subtraction = new Point3D(0,0,2*velocity.getZ());
                velocity = velocity.subtract(subtraction);
            }
        }

        if (velocity.magnitude() > 0.1) {
            Point3D delta = new Point3D(velocity.getX(), 0, velocity.getZ()).multiply(0.01);
            velocity = velocity.subtract(delta);
        } else {
            velocity = Point3D.ZERO.add(new Point3D(0,velocity.getY(),0));
        }

        if (velocity.getY() < 0) {
            velocity = velocity.add(0,0.9,0);
        } else if (velocity.getY() >= 0 && point.getY() + RADIUS < height) {
            velocity = velocity.add(0,0.3,0);
        }

        if (Math.abs(height - (point.getY() + RADIUS)) < 1 && velocity.getY() < 1 && velocity.getY() > 0) {
            velocity = velocity.subtract(0,velocity.getY(),0);
        }

        point = point.add(velocity);
        popMatrix();
    }

    void resolveCollision(Ball other) {
        if (this == other)
            return;
        if (point.distance(other.point) <= 2*RADIUS) {
            //resolve colission

            Point3D collisionVector = other.point.subtract(this.point).normalize();

            double vA = collisionVector.dotProduct(this.velocity);
            double vB = collisionVector.dotProduct(other.velocity);

            if (vA <= 0 && vB >= 0) return;

            println("Resolving collision");
            double mR = 1;
            double a = -(mR + 1);
            double b = 2 * (mR * vB + vA);
            double c = -((mR - 1) * vB * vB + 2 * vA * vB);
            double discriminant = Math.sqrt(b * b - 4 * a * c);
            double root = (-b + discriminant)/(2 * a);
            //only one of the roots is the solution, the other pertains to the current velocities
            if (root - vB < 0.01) {
                root = (-b - discriminant)/(2 * a);
            }
            this.velocity = this.velocity.add(collisionVector.multiply((vB - root)));
            other.velocity = other.velocity.add(collisionVector.multiply((root - vB)));
        }
    }

}
