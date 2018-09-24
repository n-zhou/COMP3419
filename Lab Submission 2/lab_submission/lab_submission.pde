ArrayList<PImage> texturePool;
ArrayList<Ball> balls;
java.util.Random rand;
import javafx.geometry.Point3D;

void setup() {
  size(700,700,P3D);
  texturePool = new ArrayList<PImage>();
  texturePool.add(loadImage("earth.jpg"));
  texturePool.add(loadImage("moon.jpg"));
  texturePool.add(loadImage("kevin.png"));
  balls = new ArrayList<Ball>();
  rand = new java.util.Random();
}

void draw() {
  background(0);
  for (Ball b : balls) {
    b.draw();
  }
  translate(width/2, height/2, -100);
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
  final int RADIUS = 30;
  PShape sphere;
  
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
    shape(sphere);
    point = point.add(velocity);
    
    if (point.getX() >= width) {
        if (velocity.getX() >= 0) {
          Point3D subtraction = new Point3D(2*velocity.getX(), 0,0);
          velocity = velocity.subtract(subtraction);
        }
    } else if (point.getX() <= 0) {
        if (velocity.getX() <= 0){
          Point3D addittion = new Point3D(-2*velocity.getX(), 0,0);
          velocity = velocity.add(addittion);
        }
    }
    
    if (point.getY() >= height) {
        if (velocity.getY() >= 0) {
          Point3D subtraction = new Point3D(0, 2*velocity.getY(),0);
          velocity = velocity.subtract(subtraction);
        }
    } else if (point.getY() <= 0) {
        if (velocity.getY() <= 0){
          Point3D addittion = new Point3D(0, -2*velocity.getY(),0);
          velocity = velocity.add(addittion);
        }
    }
    
    if (point.getZ() - RADIUS <= -700) {
      if (velocity.getZ() <= 0) {
        Point3D addittion = new Point3D(0,0,-2*velocity.getZ());
        velocity = velocity.add(addittion);
      }
    } else if (point.getZ() >= 0) {
      if (velocity.getZ() >= 0) {
        Point3D subtraction = new Point3D(0,0,2*velocity.getZ());
        velocity = velocity.subtract(subtraction);
      }
    }
    
    //speed decay
    
    
    
    if (point.magnitude() > 1){
      //speed decay
      velocity = velocity.multiply(0.99);
      //gravity
      velocity = velocity.add(new Point3D(0,0.1,0));
    }
    else
      velocity = Point3D.ZERO;
    
    popMatrix();
  }
  
  void collide(Ball other) {
    if (this == other)
      return;
    if (point.distance(other.point) < 30) {
      //resolve colission
    }
  }

}
