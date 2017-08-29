using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TouchScript : MonoBehaviour {

    private GameObject focusObj = null;
    private float focusx;
    private float focusy;
    private float focusz;

	// Use this for initialization
	void Start () {
        //Debug.Log("Initialised");
	}
	
	// Update is called once per frame
	void Update () {
        // Check to see if touch works.
        if (Input.touchCount > 0 && Input.GetTouch(0).phase == TouchPhase.Began){

            Debug.Log("Touch Recognised");

            focusObj = null;
            Ray ray = Camera.main.ScreenPointToRay(Input.GetTouch(0).position);
            RaycastHit hit;

            if (Physics.Raycast(ray, out hit, Mathf.Infinity))
            {
                Debug.Log("Object Touched");
                focusObj = hit.transform.gameObject;

                string link = null;

                try
                {
                    link = focusObj.GetComponentInParent<URLObject>().urlLink;
                }
                catch (Exception e) { }

                if (link != null) {
                    Application.OpenURL(link);
                }
                
            }

            // script to move object.
            //if(focusObj && Input.touchCount > 0 && Input.GetTouch(0).phase == TouchPhase.Moved)
            //{
            //    focusx = Input.GetTouch(0).deltaPosition.x / 500;
            //    focusz = 0;
            //    focusy = Input.GetTouch(0).deltaPosition.y / 500;

            //    Vector3 pos = new Vector3(focusx, focusz, focusy);
            //    focusObj.transform.position += pos;
            //}

            if(focusObj && Input.touchCount > 0 && Input.GetTouch(0).phase == TouchPhase.Ended)
            {
                focusObj = null;
            }

        }
    }
}
