using UnityEngine;

public class DroneController : MonoBehaviour
{
    [Header("Movement")]
    public float flySpeed = 50.0f;       // Speed for the giant world
    public float sprintMultiplier = 3.0f; // Hold shift to go fast

    [Header("Restraints")]
    public float worldRadius = 950f;     // Keeps you inside the 1000m sphere
    public float maxLookUp = 60f;        // 90 is straight up. 60 hides the top vortex.
    public float maxLookDown = 80f;      // 90 is straight down.

    [Header("Mouse")]
    public float mouseSensitivity = 2.0f;

    private float rotX = 0.0f;
    private float rotY = 0.0f;

    void Start()
    {
        // This locks the cursor to the center so you can look around
        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;
        
        // Match current rotation so camera doesn't snap
        Vector3 rot = transform.localRotation.eulerAngles;
        rotY = rot.y;
        rotX = rot.x;
    }

    void Update()
    {
        HandleLook();
        HandleMove();
        EnforceBoundaries();
    }

    void HandleLook()
    {
        // 1. Mouse Look (Turning your head)
        rotY += Input.GetAxis("Mouse X") * mouseSensitivity;
        rotX -= Input.GetAxis("Mouse Y") * mouseSensitivity;

        // --- RESTRICTION 1: THE NECK BRACE ---
        // Stops you from looking straight up at the ugly vortex
        rotX = Mathf.Clamp(rotX, -maxLookUp, maxLookDown); 

        transform.rotation = Quaternion.Euler(rotX, rotY, 0.0f);
    }

    void HandleMove()
    {
        // 2. WASD Movement (Walking/Flying)
        float currentSpeed = flySpeed;
        if (Input.GetKey(KeyCode.LeftShift)) currentSpeed *= sprintMultiplier;

        float x = Input.GetAxis("Horizontal"); // A and D
        float z = Input.GetAxis("Vertical");   // W and S

        // Move in the direction you are looking
        Vector3 move = transform.right * x + transform.forward * z;
        transform.position += move * currentSpeed * Time.deltaTime;
        
        // Press ESC to get your mouse back
        if (Input.GetKeyDown(KeyCode.Escape)) 
        {
            Cursor.lockState = CursorLockMode.None;
            Cursor.visible = true;
        }
        // Click to re-lock
        if (Input.GetMouseButtonDown(0))
        {
            Cursor.lockState = CursorLockMode.Locked;
            Cursor.visible = false;
        }
    }

    void EnforceBoundaries()
    {
        // --- RESTRICTION 2: THE INVISIBLE LEASH ---
        // If you try to fly past 950m (through the wall)...
        if (transform.position.magnitude > worldRadius)
        {
            // ...pull you back to the edge.
            transform.position = transform.position.normalized * worldRadius;
        }
    }
}