using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class QuadColor : MonoBehaviour {

    public Color objectColor;

    private Color defaultColor;

	// Use this for initialization
	void Start () {
        defaultColor = GetComponent<Renderer>().material.color;
    }
	
	// Update is called once per frame
	void Update () {
        //if (objectColor != defaultColor)
        //{
        //gameObject.GetComponent<Renderer>().material.color = Color.red;
        gameObject.GetComponent<Renderer>().material.color = new Color(1, 0, 0, 0.1f);
        //}
    }
}
